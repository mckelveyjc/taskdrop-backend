import mysql.connector
from mysql.connector import Error
# change this filename to "getStuffFromDB" or something like that because you're getting images from the
#  dabase here too
# make it all class based 

# gets all the tasks from the database
def getTasksFromDB():
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

            # eventually: make this work for multiple users
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

# gets five random tasks from the "recently_completed_tasks" table 
#   to be used for the AI art generation
def getTasksForPrompt():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='test_db',
            user='python',
            password='cosc4360')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute("select database()")

            record = cursor.fetchone()
            cursor.execute("select taskName from recently_completed_tasks order by rand() limit 5;")
            data = cursor.fetchall()
            return data

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# gets the image names from the generated_images database for a specific user
def getImageNames(taskUserID):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='test_db',
            user='python',
            password='cosc4360')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            cursor = connection.cursor()
            cursor.execute("select database()")
            record = cursor.fetchone()

            sqlGetImagesQuery = "select imageFileName from generated_images where taskUserID=%s"
            value = (taskUserID,)
            cursor.execute(sqlGetImagesQuery, value)
            data = cursor.fetchall()

            imgFileNameArray = []
            for imgIndex in range(len(data)):
                imgFileNameArray.append(data[imgIndex][0])

            return imgFileNameArray

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()