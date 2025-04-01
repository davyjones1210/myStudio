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

def add_project_id_to_domains_table(cursor):
    # Add project_id column to domains table if it doesn't exist
    add_column_if_not_exists(cursor, "domains", "project_id", "INT")
    
    # Add foreign key constraint to link project_id to id column of projects table
    cursor.execute("""
        ALTER TABLE domains
        ADD CONSTRAINT fk_project
        FOREIGN KEY (project_id)
        REFERENCES projects(id)
    """)
    print("Added foreign key constraint linking project_id to id column of projects table")

def main():
    cursor = connection.cursor()
    # Add project_id column to domains table and link it to projects table
    add_project_id_to_domains_table(cursor)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()