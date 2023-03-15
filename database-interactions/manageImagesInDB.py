import mysql.connector
from mysql.connector import Error
import base64
import random

# # add generated image to database
def addImgToDb(taskUserID, imageFileName):
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
# converts image from base 64 to a regular image & stores it
# for now, image is stored in /home/sr-project/user-images/{user's ID #}
# the image has a random id
# returns the image file name
def saveImage(taskUserID, imageAsBase64):
    decoded_data=base64.b64decode((imageAsBase64))
    img_id = random.randint(0,9000000000000) # not the best way to do it, I know
    #write the decoded data back to original format in file
    # img_file = open('image.jpeg', 'wb')
    # img_path = "/Users/Turing/Desktop/image-{}.jpeg".format(img_id)
    
    imageFileName = "image-{}.jpeg".format(img_id)
    # this one's the one we want (currently)
    # img_path = "/home/sr-project/user-images/user{}/image-{}.jpeg".format(taskUserID, img_id)
    img_path = "/var/www/html/user-images/user{}/{}".format(taskUserID, imageFileName)
    # img_path = "/var/www/html/user-images/user{}/image-{}.jpeg".format(taskUserID, img_id)
    img_file = open(img_path, 'wb') # to do different locations
    img_file.write(decoded_data)
    img_file.close()

    return imageFileName

# given a list of image names and a taskUserID, create an object of image urls to send back to the user
def createImageUrls(taskUserID, imgFileNameArray):
    baseUrl = "http://157.230.93.52/user-images/user{}/".format(taskUserID)
    imgUrlArray = []
    for imageFileName in imgFileNameArray:
        imgUrl = baseUrl + imageFileName
        imgUrlArray.append(imgUrl)
    return imgUrlArray

# testing
# print(createImageUrls("1", ['image-6733211111846.jpeg', 'image-6733211111846.jpeg', 'image-6733211111846.jpeg', 'image-1602370648721.jpeg']))

# addImgToDb("1", "image-6733211111846.jpeg")