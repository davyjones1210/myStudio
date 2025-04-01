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

def read_json_files(directory):
    json_data = {}
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    table_name = os.path.splitext(filename)[0]
                    json_data[table_name] = data
            except json.JSONDecodeError:
                print(f"Skipping invalid JSON file: {filename}")
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return json_data

def create_table(cursor, table_name, data):
    all_keys = set()
    for row in data:
        all_keys.update(row.keys())
    
    columns = []
    for key in all_keys:
        if key == "id":
            columns.append(f"{key} INT AUTO_INCREMENT PRIMARY KEY")
        else:
            columns.append(f"{key} VARCHAR(255)")
    columns_str = ", ".join(columns)
    sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
    cursor.execute(sql)

def insert_data(cursor, table_name, data):
    all_keys = set()
    for row in data:
        all_keys.update(row.keys())
    
    keys = list(all_keys)
    values_placeholder = ", ".join(["%s"] * len(keys))
    sql = f"INSERT INTO {table_name} ({', '.join(keys)}) VALUES ({values_placeholder})"
    
    for row in data:
        row_values = [row.get(key, 'N/A') for key in keys]
        cursor.execute(sql, tuple(row_values))

def main():
    directory = 'C:\\works\\pipeline\\database'
    json_data = read_json_files(directory)
    
    cursor = connection.cursor()
    for table_name, data in json_data.items():
        create_table(cursor, table_name, data)
        insert_data(cursor, table_name, data)
    
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()