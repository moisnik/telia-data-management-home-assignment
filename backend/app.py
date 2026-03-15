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

@app.route("/")
def index():
    projects = getprojects()
    return render_template("project_assignment.html", projects=projects)

@app.route("/submit", methods=["POST"])
def submit():
    print(request.form)

    full_name = request.form["full_name"]
    email = request.form["email"]
    projects = request.form.getlist("project")
    print(projects)

    errors = validate(full_name, email, projects)
    if(len(errors) != 0):
        print("Errors found.")
        return render_template("project_assignment.html", projects=getprojects(), errors=errors)
    

    experience_level = request.form["experience"]
    primary_technology_stack = request.form["technology_stack"]
    # To avoid errors, use .get() function for fields that do not return anything if they are left empty
    preferred_duration = request.form.get("duration", "")
    availability = request.form.get("availability", "") 
    return redirect("/")




if __name__ == "__main__":
    app.run()
    