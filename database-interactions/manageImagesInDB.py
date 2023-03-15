import mysql.connector
from mysql.connector import Error
import base64
import random

# adds a generated image filename to the "generated_images" table
def addImgToDb(taskUserID, imageFileName):
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
 
            sqlInsertImgQuery = "insert into generated_images (taskUserID, imageFileName) values (%s, %s)"
            values = (taskUserID,imageFileName)
            cursor.execute(sqlInsertImgQuery, values)
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

# takes image as a base 64 and a user's ID
# converts image from base 64 to a regular image & stores it in server
# for now, image is stored in /home/sr-project/user-images/{user's ID #}
# the image has a random id
# returns the image file name
def saveImage(taskUserID, imageAsBase64):
    decodedData=base64.b64decode((imageAsBase64))
    imgID = random.randint(0,9000000000000) # not the best way to do it (lol)
    
    imageFileName = "image-{}.jpeg".format(imgID)
    imgPath = "/var/www/html/user-images/user{}/{}".format(taskUserID, imageFileName)

    imgFile = open(imgPath, 'wb') # wb => to write at different locations
    imgFile.write(decodedData)
    imgFile.close()

    return imageFileName

# given a list of image names and a taskUserID
# creates an object of image urls to send back to the user
def createImageUrls(taskUserID, imgFileNameArray):
    baseUrl = "http://157.230.93.52/user-images/user{}/".format(taskUserID)
    imgUrlArray = []
    for imageFileName in imgFileNameArray:
        imgUrl = baseUrl + imageFileName
        imgUrlArray.append(imgUrl)
    return imgUrlArray
