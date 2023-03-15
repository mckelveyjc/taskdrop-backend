import mysql.connector
from mysql.connector import Error

# TO DO: REFACTOR TO USE connectToDB
 
# inserts a task with given user ID & default values into the tasks table
def createTask(taskUser):
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

            sqlAddTaskQuery = "insert into tasks (taskUser, taskName, taskDay, taskStart, taskEnd) values (%s, %s, %s, %s, %s)"
            values = (taskUser, "(new task)", "to-do-list", "new-task", "new-task")
            cursor.execute(sqlAddTaskQuery, values)
            connection.commit()

            # send back the taskID of the most recently created task (so we can render it on the FE)
            cursor.execute("select MAX(taskID) from tasks")
            
            data = cursor.fetchall()
            return data

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# given the taskID and a new name, updates the task name in the table
def updateTaskName(taskID, newName):
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

            sqlChangeNameQuery = "update tasks set taskName=%s where taskID=%s;"
            values = (newName, taskID)
            cursor.execute(sqlChangeNameQuery, values)
            connection.commit()
            
            data = cursor.fetchall()
            return data

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# given a taskID and a new day, updates the task day in the table
# should eventually be renamed to "updateTaskLocation"
def updateTaskDay(taskID, newDay):
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
            
            sqlUpdateQuery = "update tasks set taskDay=%s where taskID=%s;"
            values = (newDay, taskID)
            cursor.execute(sqlUpdateQuery, values)
            connection.commit()
            
            data = cursor.fetchall()
            return data

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# given information about a task
# adds that information to the "recently_completed_tasks" table
# deletes the task from the original "task" table
def completeTask(taskID, taskUser, taskName, taskDay, taskStart, taskEnd):
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
 
            sqlCompleteTaskQuery = "insert into recently_completed_tasks (taskID, taskUser, taskName, taskDay, taskStart, taskEnd) values (%s, %s, %s, %s, %s, %s)"
            values = (taskID, taskUser, taskName, taskDay, taskStart, taskEnd)
            cursor.execute(sqlCompleteTaskQuery, values)
            connection.commit()

            sqlDeleteTaskQuery = "delete from tasks where taskID=%s"
            cursor.execute(sqlDeleteTaskQuery, (taskID,))
            connection.commit()

            data = cursor.fetchall()
            return data

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# returns the number of tasks in "recently_completed_tasks"
def getNumCompletedTasks():
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
 
            sqlCountTasksQuery = "select count(taskID) FROM recently_completed_tasks"
            cursor.execute(sqlCountTasksQuery)

            data = cursor.fetchall()
            # data => [(#,)]
            cleanedData = data[0][0]
            return cleanedData

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")

# deletes all entries in the "recently_completed_database" table
def clearRecentlyCompletedTasks():
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
 
            sqlClearTasksQuery = "delete from recently_completed_tasks"
            cursor.execute(sqlClearTasksQuery)
            connection.commit()
            
            data = cursor.fetchall()
            return data

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()