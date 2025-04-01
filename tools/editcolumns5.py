import mysql.connector

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

def get_category_id(category_name):
    cursor = connection.cursor(dictionary=True)
    query = "SELECT id FROM category WHERE LOWER(name) = LOWER(%s)"
    cursor.execute(query, (category_name,))
    result = cursor.fetchone()
    cursor.close()
    return result['id'] if result else None

def update_versions_table():
    cursor = connection.cursor(dictionary=True)
    
    # Add category_id column if it doesn't exist
    cursor.execute("SHOW COLUMNS FROM versions LIKE 'category_id'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE versions ADD COLUMN category_id INT")
        print("Added category_id column to versions table")
    
    # Fetch all rows from versions table
    cursor.execute("SELECT * FROM versions")
    versions = cursor.fetchall()
    
    for version in versions:
        category_name = version['category']
        category_id = get_category_id(category_name)
        if category_id:
            cursor.execute("UPDATE versions SET category_id = %s WHERE category = %s", (category_id, category_name))
            print(f"Updated category_id for version with category {category_name}")
    
    # Drop the old category column
    cursor.execute("ALTER TABLE versions DROP COLUMN category")
    print("Dropped category column from versions table")
    
    connection.commit()
    cursor.close()

if __name__ == "__main__":
    update_versions_table()
    connection.close()