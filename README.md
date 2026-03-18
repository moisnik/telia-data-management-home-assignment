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

## Features
This is a simple form to get an employee's information and save it in the database. Employee is identified by email and according to whether they are in the database or not, their data is added or updated. <br>
Most of the fields are optional; full name, email and project selection is required. If the employee is already in the database and leaves any of the optional fields empty, their information in the database remains the same (exception about availability). Empty fields are written to the database ase None values. <br>
If a person submits theis form, session is used to save the data in the form. Clearing the form will clear the session. 

## Help and use of AI
In creating this project I got help from various resources including official documentation (Flask, PostgreSQL), other internet sources (e.g. w3schools, StackOverflow) and AI (ChatGPT). Since this was my first time creating a web application using Flask framework, ChatGPT helped mainly with establishing the connection between backend and frontend, creating the logic of data flow and session management.
