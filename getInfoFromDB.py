import mysql.connector
from mysql.connector import Error
from connectToDB import excecuteQueryOnDB

# change this filename to "getStuffFromDB" or something like that because you're getting images from the
#  dabase here too

# gets all the tasks from the database
def getTasksFromDB():
    sqlGetTasksQuery = "select * from tasks"
    data = excecuteQueryOnDB(sqlGetTasksQuery, "fetch")
    return data
        
# gets five random tasks from the "recently_completed_tasks" table 
#   to be used for the AI art generation
def getTasksForPrompt():
    sqlGetCompletedTasksQuery = "select taskName from recently_completed_tasks order by rand() limit 5;"
    data = excecuteQueryOnDB(sqlGetCompletedTasksQuery, "fetch")
    return data

# gets the image names from the generated_images database for a specific user
def getImageNames(taskUserID):
    sqlGetImagesQuery = "select imageFileName from generated_images where taskUserID=%s"
    value = (taskUserID,)
    data = excecuteQueryOnDB(sqlGetImagesQuery, "fetch", value)
    imgFileNameArray = []
    for imgIndex in range(len(data)):
        imgFileNameArray.append(data[imgIndex][0])
    return imgFileNameArray

print("")
print("tasks from db:")
print(getTasksFromDB())
print("")
print("tasks for prompt:")
print(getTasksForPrompt())
print("")
print("image names:")
print(getImageNames("1"))
print("")
