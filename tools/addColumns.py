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

def column_exists(cursor, table_name, column_name):
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM information_schema.columns
        WHERE table_name='{table_name}' AND column_name='{column_name}'
    """)
    return cursor.fetchone()[0] > 0

def add_column_if_not_exists(cursor, table_name, column_name, column_definition):
    if not column_exists(cursor, table_name, column_name):
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}")
        print(f"Added column {column_name} to {table_name}")

def add_columns_to_project_table(cursor):
    columns_to_add = {
        "id": "INT AUTO_INCREMENT PRIMARY KEY",
        "name": "VARCHAR(255)",
        "createdBy": "VARCHAR(255)",
        "createdAt": "DATETIME",
        "description": "TEXT",
        "abbreviation": "VARCHAR(50)"
    }
    for column_name, column_definition in columns_to_add.items():
        add_column_if_not_exists(cursor, "projects", column_name, column_definition)

def main():
    cursor = connection.cursor()
    # Add columns to the project table if they don't exist
    add_columns_to_project_table(cursor)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()