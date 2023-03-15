import mysql.connector
from mysql.connector import Error

def excecuteQueryOnDB(sqlQuery, values=None):
    try:
        connection = mysql.connector.connect(
        host='localhost',
        database='test_db',
        user='python',
        password='cosc4360')
        
        if connection.is_connected():
            db_Info = connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
 
            if values == None:
                cursor.execute(sqlQuery)
            else:
                cursor.execute(sqlQuery, values)
            
            connection.commit()

            data = cursor.fetchall()
            return data
    
    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()