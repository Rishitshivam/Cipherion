import mysql.connector as mycon
from src.utils.color import color

def dbcon(dbpass, dbname):
    try:
        con = mycon.connect(host='localhost', user='root', password=dbpass)
        cursor = con.cursor()
        
        cursor.execute("SHOW DATABASES LIKE %s", (dbname,))
        if cursor.fetchone():
            print(color('[INFO]', f"Database '{dbname}' already exists.", newline=True))
            print(color('[SUCCESS]', f"Connected to database '{dbname}'."))
        else:
            cursor.execute(f"CREATE DATABASE {dbname}")
            print(color('[SUCCESS]', f"Database '{dbname}' created!", newline=True))
            print(color('[SUCCESS]', f"Connected to database '{dbname}'."))
        
        con.database = dbname
        cursor.close()
        con.close()
        return True
    
    except mycon.Error as err:
        if err.errno == mycon.errorcode.ER_ACCESS_DENIED_ERROR:
            print(color('[FAIL]', "Incorrect password or access denied!", newline=True))
        else:
            print(color('[FAIL]', f"An unexpected error occurred: {err}", newline=True))
        return False

def dbsave(encdata, key, algorithm, dbpass, dbname):
    try:
        con = mycon.connect(host='localhost', user='root', password=dbpass, database=dbname)
        cursor = con.cursor()
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ctext TEXT,
            `key` BLOB,
            algorithm VARCHAR(20)
        )''')
        
        cursor.execute('''INSERT INTO data (ctext, `key`, algorithm) VALUES (%s, %s, %s)''', (encdata, key, algorithm))
        con.commit()
        recid = cursor.lastrowid
        
        cursor.close()
        con.close()
        return recid
    
    except mycon.Error as err:
        print(color('[FAIL]', f"An error occurred while saving data: {err}", newline=True))
        return None

def dbget(inrec, dbpass, dbname):
    try:
        con = mycon.connect(host='localhost', user='root', password=dbpass, database=dbname)
        cursor = con.cursor()
        
        cursor.execute('''SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = 'data' ''', (dbname,))
        if cursor.fetchone()[0] == 0:
            print(color('[INFO]', "Make sure to encrypt data before trying to decrypt.", newline=True))
            print(color('[FAIL]', f"No data exists in the database '{dbname}'!"))
            cursor.close()
            con.close()
            return None
        
        cursor.execute('''SELECT ctext, `key`, algorithm FROM data WHERE id = %s''', (inrec,))
        res = cursor.fetchone()
        
        cursor.close()
        con.close()

        return res
    
    except mycon.Error as err:
        print(color('[FAIL]', f"An error occurred while retrieving data: {err}", newline=True))
        return None