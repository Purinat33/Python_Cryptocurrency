# Define mysql stuff in here instead of having
# to perform everything manually in app.py

# A basis for accessessing MySQL

from app import mysql, session

class Table():
    # Want
    # users = Table('users', 'name', 'username', 'email', 'password')
    def __init__(self, table_name, *args) -> None:
        self.table = table_name
        self.columns = "(%s)" %",".join(args)
        
        if isNewTable(table_name):
            cur = mysql.connection.cursor()
            cur.execute('CREATE TABLE %s%s' %(self.table, self.columns))
            cur.close()
    
    def getAll(self):
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s" %self.table)
        data = cur.fetchall(); return data

    
    def getSingle(self, search, value):
        data = {}; cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s WHERE %s = \"%s\"" %(self.table, search, value))
        if result > 0: data = cur.fetchone()
        cur.close(); return data
    
    def deleteSingle(self, search, value):
        cur = mysql.connection.cursor()
        cur.execute("DELETE from %s where %s = \"%s\"" %(self.table, search, value))
        mysql.connection.commit(); cur.close()
    
    def deleteAll(self):
        self.drop() #remove table and recreate
        self.__init__(self.table, *self.columnsList)
    
    def drop(self):
        cur = mysql.connection.cursor()
        cur.execute("DROP TABLE %s" %self.table)
        cur.close()
    
    def insert(self, *args):
        data = ""
        for arg in args: #convert data into string mysql format
            data += "\"%s\"," %(arg)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO %s%s VALUES(%s)" %(self.table, self.columns, data[:len(data)-1]))
        mysql.connection.commit()
        cur.close()
            
#execute mysql code from python
def sql_raw(execution):
    cur = mysql.connection.cursor()
    cur.execute(execution)
    mysql.connection.commit()
    cur.close()

def isNewTable(tableName):
    cur = mysql.connection.cursor()
    try:
        result = cur.execute('SELECT * FROM %s' %tableName)
        cur.close()
    except:
        return True
    else:
        return False
    
def isNewUser(username):
    #access the users table and get all values from column "username"
    users = Table("users", "name", "email", "username", "password")
    data = users.getall()
    usernames = [user.get('username') for user in data]

    return False if username in usernames else True