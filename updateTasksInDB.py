import mysql.connector
from mysql.connector import Error

# eventually: rework this into a class so I can reuse sql connection code in __init__
def updateTaskDay(taskID, newDay):
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
            # we'll do the below eventually. for some reason it keep returning null
            # cursor.execute("select * from tasks where taskUser=?", (1))
            # we'll do the below instead for now
            
            cursor.execute("update tasks set taskDay=%s where taskID=%s;" (newDay, taskID))
            # cursor.execute("update tasks set taskDay='wednesday' where taskID=2;")
            
            # testing
            cursor.execute("select * from tasks")
            
            data = cursor.fetchall()
            return data
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")