import pymysql 

class myDatabase(object):

    def __init__(self):
		
        self.hot = "127.0.0.1"
        self.user = "root"
        self.password = None
        self.db = "test-db-kd6"

        self.conn = None
		
    def connect(self):
        self.conn = pymysql.connect( 
            host=self.hot, 
            user=self.user, 
            # password =self.password, 
            db=self.db, 
            cursorclass=pymysql.cursors.DictCursor,
        ) 
    
    def query(self, table, columns="*", conditions=None):
        self.connect()
        cursor = self.conn.cursor()
        sql = f"SELECT {columns} FROM {table}"
        if conditions:
            sql += f" WHERE {conditions}"
        cursor.execute(sql)
        result = cursor.fetchall()
        self.conn.close()
        return result


    
    def searchAll(self, table):
    
        cursor= self.conn.cursor() 
  
        # execute your query 
        cursor.execute("SELECT * FROM {}".format(table)) 
  
        # fetch all the matching rows  
        result = cursor.fetchall() 
        print("Printing result of fetch all: ", result)
  
        return result
    
    
    def insert(self, table, data):
        cursor = self.conn.cursor()

        # Check if the table has an 'id' column
        cursor.execute(f"SHOW COLUMNS FROM {table} LIKE 'id'")
        id_column_exists = cursor.fetchone() is not None

        keys = ", ".join(data.keys())
        values = ", ".join(["%s"] * len(data))

        if id_column_exists:
            id = self.getLatestID(table)
            next_id = id + 1
            sql = f'INSERT INTO {table} (id, {keys}) VALUES (%s, {values})'
            cursor.execute(sql, (next_id, *data.values()))
        else:
            sql = f'INSERT INTO {table} ({keys}) VALUES ({values})'
            cursor.execute(sql, tuple(data.values()))

        self.conn.commit()
        self.conn.close()
    
    # def getlatestInsert(self, table):

    #     return data
    
    def getLatestID(self, table):
        # This method should return the latest ID from the table
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT MAX(id) as max_id FROM {table}")
        result = cursor.fetchone()
        return result['max_id'] if result['max_id'] is not None else 200



    # def mysqlconnect(): 
    #     # To connect MySQL database 
    #     conn = pymysql.connect( 
    #         host='localhost', 
    #         user='root', 
    #         password = "pass", 
    #         db='College', 
    #         ) 
        
    #     cur = conn.cursor() 
    #     cur.execute("select @@version") 
    #     output = cur.fetchall() 
    #     print(output) 
        
        # To close the connection 
        # conn.close() 

# # Driver Code 
# if __name__ == "__main__" :
#     pass
# 	# mysqlconnect()
