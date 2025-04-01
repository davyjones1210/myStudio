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

def delete_department_column():
    cursor = connection.cursor()
    
    # Drop all foreign key constraints involving the department column
    cursor.execute("""
        SELECT CONSTRAINT_NAME
        FROM information_schema.KEY_COLUMN_USAGE
        WHERE TABLE_NAME = 'versions' AND COLUMN_NAME = 'department'
    """)
    constraints = cursor.fetchall()
    for constraint in constraints:
        cursor.execute(f"ALTER TABLE versions DROP FOREIGN KEY {constraint['CONSTRAINT_NAME']}")
        print(f"Dropped foreign key constraint {constraint['CONSTRAINT_NAME']} from versions table")
    
    # Drop the index on the department column if it exists
    cursor.execute("SHOW INDEX FROM versions WHERE Column_name = 'department'")
    index = cursor.fetchone()
    if index:
        cursor.execute(f"ALTER TABLE versions DROP INDEX {index[2]}")  # Index name is in the third column
        print(f"Dropped index {index[2]} from versions table")
    
    # Drop the old department column
    cursor.execute("ALTER TABLE versions DROP COLUMN department")
    print("Dropped department column from versions table")
    
    connection.commit()
    cursor.close()

def add_foreign_key():
    cursor = connection.cursor()
    
    # Ensure the department_id column exists in the departments table
    cursor.execute("SHOW COLUMNS FROM departments LIKE 'department_id'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE departments ADD COLUMN department_id INT AUTO_INCREMENT PRIMARY KEY")
        print("Added department_id column to departments table")
    
    # Add foreign key constraint to link department_id in versions table to department_id in departments table
    cursor.execute("""
        ALTER TABLE versions
        ADD CONSTRAINT fk_department_id
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
    """)
    print("Added foreign key constraint linking department_id in versions table to department_id in departments table")
    
    connection.commit()
    cursor.close()

if __name__ == "__main__":
    delete_department_column()
    add_foreign_key()
    connection.close()