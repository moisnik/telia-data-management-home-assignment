CREATE TABLE employees(
	id serial PRIMARY KEY,
	first_name varchar(50) NOT NULL,
	last_name varchar(50) NOT NULL,
	email VARCHAR(200) NOT NULL UNIQUE,
    experience_level VARCHAR(50),
    primary_technology_stack VARCHAR(50),
    preferred_duration VARCHAR(50),
	availability boolean NOT NULL DEFAULT FALSE);

ALTER TABLE employees
ADD COLUMN availability BOOLEAN NOT NULL DEFAULT FALSE;

CREATE TABLE skills(
	id serial PRIMARY KEY,
	skill varchar(50) NOT NULL UNIQUE);

CREATE TABLE projects(
	id serial PRIMARY KEY,
	project_name varchar(200) NOT NULL UNIQUE);

CREATE TABLE employee_skills(
	id serial NOT NULL PRIMARY KEY,
	employee_id int NOT NULL,
	skill varchar(50) NOT NULL);

CREATE TABLE employee_projects(
	id serial NOT NULL PRIMARY KEY,
	employee_id int NOT NULL,
	project varchar(200) NOT NULL);

ALTER TABLE employee_skills ADD CONSTRAINT fk_employee_skill
FOREIGN KEY (employee_id)
REFERENCES employees(id)
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE employee_skills ADD CONSTRAINT fk_skill_employee
FOREIGN KEY (skill)
REFERENCES skills(skill)
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE employee_projects ADD CONSTRAINT fk_employee_project
FOREIGN KEY (employee_id)
REFERENCES employees(id)
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE employee_projects ADD CONSTRAINT fk_project_employees
FOREIGN KEY (project)
REFERENCES projects(project_name)
ON DELETE CASCADE ON UPDATE CASCADE;
