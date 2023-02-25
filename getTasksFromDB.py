import mysql.connector
from mysql.connector import Error
# change this filename to "getStuffFromDB" or something like that because you're getting images from the
#  dabase here too

# needs to be renamed to "get all tasks from db"
def getTasksFromDB():
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

# this function gets three random tasks from the "recently_completed_tasks" table 
# will be used in generateArt. 
# for now I'm getting the tasks from the normal "tasks" table just for testing
# eventually we should orchestrate this so that it doesn't get repeated tasks
def getTasksForPrompt():
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
            cursor.execute("select database()")
            record = cursor.fetchone()

            # now let's select three random tasks
            # cursor.execute("select taskName from tasks order by rand() limit 3;")
            cursor.execute("select taskName from recently_completed_tasks order by rand() limit 3;")
            data = cursor.fetchall()
            return data
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")

# this function gets the image names from the database
def getImageNames(taskUserID):
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
            # print("MySQL connection is closed")

# testing
print(getImageNames("1"))