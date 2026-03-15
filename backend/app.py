from flask import Flask, render_template
import psycopg2

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

@app.route("/")
def index():
    projects = getprojects()
    return render_template("project_assignment.html", projects=projects)

if __name__ == "__main__":
    app.run()
    