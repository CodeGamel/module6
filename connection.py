import mysql.connector
from mysql.connector import Error

database = 'e_com'
user = 'root'
password ='lololo'
host = 'localhost'

def connection():

    try:
        conn = mysql.connector.connect( 
            database = 'e_com',
            user = 'root',
            password = 'lololo',
            host = 'localhost'
            )
        
        if conn.is_connected():
            print("Successfully connected to the database!")
            return conn
        
    except Error as e:
        print(f"Error: {e}")
        return None