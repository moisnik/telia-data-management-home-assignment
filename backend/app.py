from flask import Flask, render_template, request, redirect
import psycopg2
import re

app = Flask(__name__)

DB_CONFIG = {
    "host": "localhost",
    "dbname": "projects",
    "user": "postgres",
    "password": input("enter password:"),
    "port": "5433"
}

def getprojects():
    """ Function to get all project names from the database 
        in order to show them dynamically in the web app."""
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM projects;")
    projects = cursor.fetchall()

    cursor.close()
    connection.close()

    return projects

def validate(full_name, email, projects):
    """ Function to validate the user's input:
        check if they inserted at least 2 names, a valid email address and selected at least one project.
        Collect occurring errors in an array and return it."""
    errors = []
    if len(full_name.split(" ")) < 2:
        errors.append("Please enter your full name.")

    email_pattern = r"^[a-zA-Z0–9._+-]+@[a-zA-Z0–9.+-]+\.[a-zA-Z]+$"
    if email:
        if not re.match(email_pattern, email):
            errors.append("Please add a valid email address.")
    
    if(len(projects)==0):
        errors.append("Please choose at least one project.")

    return errors

def check_profile(email):
    """ Check if the person who submitted the form is already in the database.
        Use email since it is a unique value."""
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM employees WHERE email = %s;", (email,))
    existing_employee = cursor.fetchone()

    cursor.close()
    connection.close()

    if existing_employee:
        return True

    return False

def update_skills(skills):
    """ Use the submitted list of skills to update the table.
        Skills are unique - if it is alreay in the database, do nothing."""
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    for skill in skills:
        cursor.execute("""
                       INSERT INTO skills (skill)
                       VALUES (%s)
                       ON CONFLICT (skill) DO NOTHING
                       """, (skill,))

    connection.commit()
    cursor.close()
    connection.close()

def update_data(full_name, email, projects, experience_level, primary_technology_stack, preferred_duration, availability, skills):
    """ If the person is already in the database, update their data.
        If a field is left empty, keep the old value, with an exception about the availability status.
        Replace old projects with new selected ones and add new skills."""
    first_name, last_name = full_name.split(" ", 1)
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    cursor.execute(""" 
                   UPDATE employees
                   SET first_name = %s,
                   last_name = %s,
                   experience_level = COALESCE(%s, experience_level),
                   primary_technology_stack = COALESCE(%s, primary_technology_stack),
                   preferred_duration = COALESCE(%s, preferred_duration),
                   availability = %s
                   WHERE email = %s
                   RETURNING id;
                   """, (first_name, last_name, experience_level, primary_technology_stack, preferred_duration, availability, email))
    
    employee_id = cursor.fetchone()[0]

    cursor.execute("DELETE FROM employee_projects WHERE employee_id = %s", (employee_id,))

    for project_id in projects:
        cursor.execute("""
                       INSERT INTO employee_projects (employee_id, project_id)
                       VALUES (%s, %s)
                       """, (employee_id, project_id))
        
    for skill in skills:
        cursor.execute("""
                       SELECT * FROM employee_skills 
                       WHERE employee_id = %s AND skill = %s 
                       """, (employee_id, skill))
        
        if cursor.fetchone():
            continue

        cursor.execute("""
                       INSERT INTO employee_skills (employee_id, skill)
                       VALUES (%s, %s)
                       """, (employee_id, skill))
    connection.commit()
    cursor.close()
    connection.close()

def insert_data(full_name, email, projects, experience_level, primary_technology_stack, preferred_duration, availability, skills):
    """ If the person is not already in the database, insert their data.
        Fill in tables about skills and projects."""
    first_name, last_name = full_name.split(" ", 1)
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    cursor.execute("""
                   INSERT INTO employees (first_name, last_name, email, experience_level, primary_technology_stack, preferred_duration, availability)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   RETURNING id
                   """, (first_name, last_name, email, experience_level, primary_technology_stack, preferred_duration, availability))

    employee_id = cursor.fetchone()[0]
    for project_id in projects:
        cursor.execute("""
                       INSERT INTO employee_projects (employee_id, project_id)
                       VALUES (%s, %s)
                       """, (employee_id, project_id))
        
    for skill in skills:
        cursor.execute("""
                       INSERT INTO employee_skills (employee_id, skill)
                       VALUES (%s, %s)
                       """, (employee_id, skill))
    connection.commit()
    cursor.close()
    connection.close()


def clean_skills(skills):
    skills = skills.split(",")
    for skill in skills:
        skill = skill.strip().lower()
    return skills


@app.route("/")
def index():
    projects = getprojects()
    return render_template("project_assignment.html", projects=projects)

@app.route("/submit", methods=["POST"])
def submit():
    """ Function to handle form submissions:
        extract information, validate name, email and projects, update database or add a new employee."""
    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    projects = request.form.getlist("project")

    errors = validate(full_name, email, projects)
    if(len(errors) != 0):
        print("Errors found.")
        return render_template("project_assignment.html", projects=getprojects(), errors=errors)
    
    # If optional fields are left empty, replace them with None for cleaner database insertion
    experience_level = request.form.get("experience", "").strip() or None
    primary_technology_stack = request.form.get("technology_stack", "").strip() or None
    preferred_duration = request.form.get("duration", "").strip() or None
    skills = request.form.get("skills", "") or None
    availability = "availability" in request.form

    if skills:
        skills = clean_skills(skills)
        update_skills(skills)

    existing_employee = check_profile(email)
    if existing_employee:
        update_data(full_name, email, projects, experience_level, primary_technology_stack, preferred_duration, availability, skills)
    else: 
        insert_data(full_name, email, projects, experience_level, primary_technology_stack, preferred_duration, availability, skills)

    return redirect("/")

if __name__ == "__main__":
    app.run()
    