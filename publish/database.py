import pymysql 

class myDatabase(object):

    def __init__(self):
		
        self.hot = "127.0.0.1"
        self.user = "root"
        self.password = None
        self.db = "kunaldb"

        self.conn = None
		
    def connect(self):
        self.conn = pymysql.connect( 
            host=self.hot, 
            user=self.user, 
            # password =self.password, 
            db=self.db, 
        ) 
    
    def searchAll(self, table):
    
        cursor= self.conn.cursor() 
  
        # execute your query 
        cursor.execute("SELECT * FROM {}".format(table)) 
  
        # fetch all the matching rows  
        result = cursor.fetchall() 
  
        return result
    
    def insert(self, table, value):
        # Inserts what table you want to insert and what value
        # Bonus: Add multiple values
        pass

    def query(self, table, key, value):
        # [{'email': 'kunal@gmail.com', 'id': 101, 'name': 'kunal', 'password': 'kunal'},
        #     {'email': 'sachin@gmail.com',
        #   'id': 102,
        #   'name': 'sachin',
        #   'password': 'password'}]
        pass

    def mysqlconnect(): 
        # To connect MySQL database 
        conn = pymysql.connect( 
            host='localhost', 
            user='root', 
            password = "pass", 
            db='College', 
            ) 
        
        cur = conn.cursor() 
        cur.execute("select @@version") 
        output = cur.fetchall() 
        print(output) 
        
        # To close the connection 
        conn.close() 

# Driver Code 
if __name__ == "__main__" : 
	mysqlconnect()
