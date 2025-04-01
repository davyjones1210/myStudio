import mysql.connector
import os
import json

# One time tool to connect to a blank database and transfer all the json file data to SQL database

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test-db-kd2"
)

if connection.is_connected():
    print("Successfully connected")
else:
    print("Failed to connect")

def add_departments_table(cursor):
    # Create the departments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            department_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255)
        )
    """)
    
    # Insert department names with IDs starting from 500
    departments = [
        "Modeling", "Rigging", "LookDev", "Layout",
        "Animation", "Rendering", "Compositing"
    ]
    
    sql = "INSERT INTO departments (department_id, name) VALUES (%s, %s)"
    for i, name in enumerate(departments, start=500):
        cursor.execute(sql, (i, name))

def main():
    cursor = connection.cursor()
    # Add the departments table and insert data
    add_departments_table(cursor)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()