# Telia data management developer internship - home assignment
The goal of this assignment was to create a simple web application for managing internal project assignments.
Employees should be able to register their profile, select projects they're interested in, and update their information as needed.

## Setup instructions
* Clone the contents of this repository: `git clone https://github.com/moisnik/telia-data-management-home-assignment`
* Install the needed packages: `pip install flask psycopg2 beautifulsoup4`
* Set up the database:
  - Log in to PostgreSQL and create a new database (e.g. "projects")
  - Use the dump file to get the structure and data
* Run the application bu running the `app.py` file
  - To make a connection with the database, enter in terminal your database name (projects), PostgreSQL username, password and port number (might be 5432)
* Open app in browser: `http://127.0.0.1:5000/`
