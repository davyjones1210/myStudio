import mysql.connector
import os
import json

# One time tool to connect to a blank database and transfer all the json file data to SQL database

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test-db-kd3"
)

if connection.is_connected():
    print("Successfully connected to database:", connection.database)
else:
    print("Failed to connect")

def column_exists(cursor, table_name, column_name):
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM information_schema.columns
        WHERE table_schema='{connection.database}' AND table_name='{table_name}' AND column_name='{column_name}'
    """)
    return cursor.fetchone()[0] > 0

def add_column_if_not_exists(cursor, table_name, column_name, column_definition):
    if not column_exists(cursor, table_name, column_name):
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}")
        print(f"Added column {column_name} to {table_name}")
    else:
        print(f"Column {column_name} already exists in {table_name}")

def add_password_to_artists_table(cursor):
    # Add password column to artists table if it doesn't exist
    add_column_if_not_exists(cursor, "artists", "password", "VARCHAR(255)")

def main():
    cursor = connection.cursor()
    # Print the current database name
    cursor.execute("SELECT DATABASE()")
    current_database = cursor.fetchone()[0]
    print(f"Current database: {current_database}")
    
    # Print the structure of the artists table
    cursor.execute("DESCRIBE artists")
    table_structure = cursor.fetchall()
    print("Artists table structure:")
    for column in table_structure:
        print(column)
    
    # Add password column to artists table
    add_password_to_artists_table(cursor)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()