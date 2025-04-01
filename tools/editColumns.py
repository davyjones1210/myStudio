import mysql.connector
import os
import json

# One time tool to connect to a blank database and transfer all the json file data to SQL database

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test-db-kd5"
)

if connection.is_connected():
    print("Successfully connected")
else:
    print("Failed to connect")

def get_project_id(project_name):
    cursor = connection.cursor(dictionary=True)
    query = "SELECT id FROM projects WHERE name = %s"
    cursor.execute(query, (project_name,))
    result = cursor.fetchone()
    cursor.close()
    return result['id'] if result else None

def update_versions_table():
    cursor = connection.cursor(dictionary=True)
    
    # Add project_id column if it doesn't exist
    cursor.execute("SHOW COLUMNS FROM versions LIKE 'project_id'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE versions ADD COLUMN project_id INT")
        print("Added project_id column to versions table")
    
    # Fetch all rows from versions table
    cursor.execute("SELECT * FROM versions")
    versions = cursor.fetchall()
    
    for version in versions:
        project_name = version['project']
        project_id = get_project_id(project_name)
        if project_id:
            cursor.execute("UPDATE versions SET project_id = %s WHERE project = %s", (project_id, project_name))
            print(f"Updated project_id for version with project {project_name}")
    
    # Drop the old project column
    cursor.execute("ALTER TABLE versions DROP COLUMN project")
    print("Dropped project column from versions table")
    
    connection.commit()
    cursor.close()

def add_project_id_foreign_key():
    cursor = connection.cursor()
    
    # Ensure the id column exists in the projects table
    cursor.execute("SHOW COLUMNS FROM projects LIKE 'id'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE projects ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
        print("Added id column to projects table")
    
    # Add foreign key constraint to link project_id in versions table to id in projects table
    cursor.execute("""
        ALTER TABLE versions
        ADD CONSTRAINT fk_project_id
        FOREIGN KEY (project_id)
        REFERENCES projects(id)
    """)
    print("Added foreign key constraint linking project_id in versions table to id in projects table")
    
    connection.commit()
    cursor.close()

if __name__ == "__main__":
    update_versions_table()
    add_project_id_foreign_key()
    connection.close()