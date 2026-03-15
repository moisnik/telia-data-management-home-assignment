from bs4 import BeautifulSoup
import psycopg2

HTML_FILE = "./project_assignment.html"

DB_CONFIG = {
    "host": "localhost",
    "dbname": "projects",
    "user": "postgres",
    "password": input("enter password:"),
    "port": "5433"
}

def extract_projects_from_html(file):
    projects = []
    with open(file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    selector = soup.find("select", multiple=True)
    options = selector.find_all("option")

    for option in options:
        projects.append(option.get_text(strip=True))

    return projects

def insert_projects(projects):
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    for project in projects:
        cursor.execute(
            """
            INSERT INTO projects (project_name)
            VALUES (%s)
            ON CONFLICT (project_name) DO NOTHING;
            """,
            (project,)
        )

    connection.commit()
    cursor.close()
    connection.close()

def main():
    projects = extract_projects_from_html(HTML_FILE)
    insert_projects(projects)
    print("Projects imported successfully.")

if __name__ == "__main__":
    main()