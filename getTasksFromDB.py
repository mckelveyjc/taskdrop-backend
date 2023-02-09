import mysql.connector
from mysql.connector import Error

def getTasksFromDB(userName, userPassword):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='test_db',
            user='python',
            password='cosc4360')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            # print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            # print("You're connected to database: ", record)
            cursor.execute("select userName from users where userName=%s and userPassword=%s", (userName, userPassword))
            data = cursor.fetchall()
            if not data:
                print ('incorrect username or password')
                return False
            else:
                print ('welcome!')
                return True
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")