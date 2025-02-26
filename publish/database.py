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
            cursorclass=pymysql.cursors.DictCursor,
        ) 
    
    def searchAll(self, table):
    
        cursor= self.conn.cursor() 
  
        # execute your query 
        cursor.execute("SELECT * FROM {}".format(table)) 
  
        # fetch all the matching rows  
        result = cursor.fetchall() 
  
        return result
    
    def insert(self, table, data):
        # Inserts what table you want to insert and what value
        # Bonus: Add multiple values

        cursor = self.conn.cursor()

        keys = ", ".join(list(data.keys()))
        values = "\'{}\'".format("\', \'".join(list(data.values())))

        id = self.getLatestID(table)
        # name, createdBy
        # test_1, Owner
        next_id = id + 1

        cursor.execute('INSERT INTO project (id, {}) VALUES ({}, {})'.format(keys, next_id, values))

        self.conn.commit()
        self.conn.close()
    
    def getlatestInsert(self, table):

        return data
    
    def getLatestID(self, table):
        # data = getlatestInsert(table)
        # return data["id"] # or data[0]
        # Find out how to setup auto increment in GUI. Working on code is first preference to get next ID
        # Such that 

        return 200

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
    pass
	# mysqlconnect()
