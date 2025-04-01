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

def add_foreign_key():
    cursor = connection.cursor()
    
    # Ensure the category_id column exists in the category table
    cursor.execute("SHOW COLUMNS FROM category LIKE 'id'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE category ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
        print("Added id column to category table")
    
    # Add foreign key constraint to link category_id in versions table to id in category table
    cursor.execute("""
        ALTER TABLE versions
        ADD CONSTRAINT fk_category_id
        FOREIGN KEY (category_id)
        REFERENCES category(id)
    """)
    print("Added foreign key constraint linking category_id in versions table to id in category table")
    
    connection.commit()
    cursor.close()

if __name__ == "__main__":
    add_foreign_key()
    connection.close()