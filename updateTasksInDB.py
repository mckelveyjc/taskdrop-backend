import mysql.connector
from mysql.connector import Error
# eventually: rework this into a class so I can reuse sql connection code in __init__

# adds taskUser & taskLocation (as "to-do") but leaves everything else blank
def createTask(taskUser):
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
            
            sqlAddTaskQuery = "insert into tasks (taskUser, taskName, taskDay, taskStart, taskEnd) values (%s, %s, %s, %s, %s)"
            values = (taskUser, "to-do", "to-do-list", "new-task", "new-task")
            # change "to-do" to "(new task)" or whatever it is on the front-end next time you edit this file
            cursor.execute(sqlAddTaskQuery, values)
            connection.commit()

            # send back the taskID of the most recently created task (so we can render it on the FE)
            cursor.execute("select MAX(taskID) from tasks")
            # testing
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

# updates the name of the task in the DB
def updateTaskName(taskID, newName):
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
            sqlChangeNameQuery = "update tasks set taskName=%s where taskID=%s;"
            values = (newName, taskID)
            cursor.execute(sqlChangeNameQuery, values)
            connection.commit()

            # testing
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
            
            sqlUpdateQuery = "update tasks set taskDay=%s where taskID=%s;"
            values = (newDay, taskID)
            # sql_update_query = """update tasks set taskDay = 'wednesday' where taskID = 2"""
            cursor.execute(sqlUpdateQuery, values)
            connection.commit()

            # testing
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

# adds taskUser & taskLocation (as "to-do") but leaves everything else blank
def completeTask(taskID, taskUser, taskName, taskDay, taskStart, taskEnd):
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
            
            # sqlCompleteTaskQuery = "insert into recently_completed_tasks (taskID, taskUser, taskName, taskDay, taskStart, taskEnd) values (%s, %s, %s, %s, %s, %s)"
            # values = (taskID, taskUser, taskName, taskDay, taskStart, taskEnd)
            # cursor.execute(sqlCompleteTaskQuery, values)
            # connection.commit()

            sqlDeleteTaskQuery = "delete from tasks where taskID=%s"
            values = taskID
            cursor.execute(sqlDeleteTaskQuery, values)
            connection.commit()

            data = cursor.fetchall()
            return data

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")

# createTask("1")
completeTask("159", "1", "to-do", "to-do-list", "new-task", "new-task")