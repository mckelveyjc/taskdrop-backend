import mysql.connector
from mysql.connector import Error

def getTasksFromDB(taskUserID):
    taskUserID = int(taskUserID)
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
            cursor.execute("select * from tasks where taskUser=%i;", (1))
            # cursor.execute("select * from tasks")
            data = cursor.fetchall()
            return data
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")