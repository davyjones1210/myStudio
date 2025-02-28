import mysql.connector
import os
import json

# One time tool to connect to a blank database and transfer all the json file data to SQL database

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test-db-kd6"
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

def add_index_if_not_exists(cursor, table_name, column_name):
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM information_schema.statistics
        WHERE table_schema=DATABASE() AND table_name='{table_name}' AND column_name='{column_name}'
    """)
    if cursor.fetchone()[0] == 0:
        cursor.execute(f"CREATE INDEX idx_{column_name} ON {table_name} ({column_name})")
        print(f"Added index on {column_name} in {table_name}")

def add_department_to_domains_table(cursor):
    # Ensure the department column exists in the versions table
    add_column_if_not_exists(cursor, "versions", "department", "VARCHAR(255)")
    add_index_if_not_exists(cursor, "versions", "department")
    
    # Add department column to domains table if it doesn't exist
    add_column_if_not_exists(cursor, "domains", "department", "VARCHAR(255)")
    
    # Add foreign key constraint to link department to department column of versions table
    cursor.execute("""
        ALTER TABLE domains
        ADD CONSTRAINT fk_department
        FOREIGN KEY (department)
        REFERENCES versions(department)
    """)
    print("Added foreign key constraint linking department to department column of versions table")

def main():
    cursor = connection.cursor()
    # Add department column to domains table and link it to versions table
    add_department_to_domains_table(cursor)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()