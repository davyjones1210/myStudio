import mysql.connector

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
    
    # Drop all foreign key constraints involving the department column in the versions table
    cursor.execute("""
        SELECT CONSTRAINT_NAME, TABLE_NAME
        FROM information_schema.KEY_COLUMN_USAGE
        WHERE REFERENCED_TABLE_NAME = 'versions' AND REFERENCED_COLUMN_NAME = 'department'
    """)
    constraints = cursor.fetchall()
    for constraint in constraints:
        try:
            cursor.execute(f"ALTER TABLE {constraint[1]} DROP FOREIGN KEY {constraint[0]}")
            print(f"Dropped foreign key constraint {constraint[0]} from table {constraint[1]}")
        except mysql.connector.errors.ProgrammingError as e:
            print(f"Error dropping foreign key constraint {constraint[0]} from table {constraint[1]}: {e}")
    
    # Drop the index on the department column if it exists
    cursor.execute("SHOW INDEX FROM versions WHERE Column_name = 'department'")
    indexes = cursor.fetchall()
    for index in indexes:
        try:
            cursor.execute(f"ALTER TABLE versions DROP INDEX {index[2]}")  # Index name is in the third column
            print(f"Dropped index {index[2]} from versions table")
        except mysql.connector.errors.ProgrammingError as e:
            print(f"Error dropping index {index[2]} from versions table: {e}")
    
    # Drop the old department column
    try:
        cursor.execute("ALTER TABLE versions DROP COLUMN department")
        print("Dropped department column from versions table")
    except mysql.connector.errors.ProgrammingError as e:
        print(f"Error dropping department column from versions table: {e}")
    
    connection.commit()
    cursor.close()

if __name__ == "__main__":
    delete_department_column()
    connection.close()