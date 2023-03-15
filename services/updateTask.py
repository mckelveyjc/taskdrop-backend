import logging
import json
import ast
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs
from generateArt import openAIArtRequest
from updateTasksInDB import createTask, updateTaskName, updateTaskDay, completeTask, getNumCompletedTasks, clearRecentlyCompletedTasks
from manageImagesInDB import addImgToDb, saveImage

logging.basicConfig(level=logging.DEBUG)

# this service deals with task creation, updating task names / days, and completing tasks
class BaseAppService(BaseHTTPRequestHandler):

    HTTP_STATUS_RESPONSE_CODES = {
        'OK': HTTPStatus.OK,
        'FORBIDDEN': HTTPStatus.FORBIDDEN,
        'NOT_FOUND': HTTPStatus.NOT_FOUND,
    }

    def extract_POST_Body(self):
        # The content-length HTTP header is where our POST data will be in the request. So we'll need to
        # read the data using an IO input buffer stream built into the http.server module.
        postBodyLength = int(self.headers['content-length'])
        postBodyString = self.rfile.read(postBodyLength)
        postBodyDict = json.loads(postBodyString)
        logging.info('POST Body received: ' +
                     json.dumps(postBodyDict, indent=4, sort_keys=True))
        return postBodyDict
    
    def do_POST(self):
        path = self.path
        # Extract the POST body data from the HTTP request, and store it into a Python
        # dictionary we can utilize inside of any of our POST endpoints.
        postBody = self.extract_POST_Body()
        status = self.HTTP_STATUS_RESPONSE_CODES['NOT_FOUND']

        responseBody = {}
        if path == '/':
            status = self.HTTP_STATUS_RESPONSE_CODES['OK']
            responseBody['data'] = 'Hello world'
        
        elif path == '/update-task/create-task':
            status = self.HTTP_STATUS_RESPONSE_CODES['OK']
            dataString = json.dumps(postBody)
            response = ast.literal_eval(dataString)

            # adds a task with default data into db
            responseBody = createTask(response["taskUser"])

        elif path == '/update-task/update-name':
            status = self.HTTP_STATUS_RESPONSE_CODES['OK']
            dataString = json.dumps(postBody)
            response = ast.literal_eval(dataString)

            updateTaskName(response["taskID"], response["newName"])

        # should be: update-task-location for clarity
        elif path == '/update-task/update-day':
            status = self.HTTP_STATUS_RESPONSE_CODES['OK']
            dataString = json.dumps(postBody)
            response = ast.literal_eval(dataString)
            
            updateTaskDay(response["taskID"], response["newDay"])
        
        elif path == '/update-task/complete-task':
            status = self.HTTP_STATUS_RESPONSE_CODES['OK']
            dataString = json.dumps(postBody)
            response = ast.literal_eval(dataString)

            # we need all of the task information here so we can move it all to 
            #   recently_completed_tasks
            completeTask(
                response["taskID"], 
                response["taskUser"],
                response["taskName"],
                response["taskDay"],
                response["taskStart"],
                response["taskEnd"])
            
            numCompletedTasks = getNumCompletedTasks()
            if (numCompletedTasks >= 5): # >= instead of == here in case of overflow
                # create a piece of art based on tasks                
                generatedImageData = openAIArtRequest()

                # get the base64 of that image from the dictionary             
                generatedImageBase64 = generatedImageData["data"][0]["b64_json"]
    
                # saveImage returns the image filename
                imageFileName = saveImage("1", generatedImageBase64)

                # add that filename to the generated_images database
                addImgToDb("1", imageFileName)
 
                # clear recently_completed_tasks
                # doing this so we only use the most recent five tasks to create the art instead of all completed tasks ever
                clearRecentlyCompletedTasks()
    
                # tell the frontend that the art is ready
                responseBody["artReady"] = True

            else:
                # if the user hasn't completed five tasks, they don't get any art
                responseBody["artReady"] = False

        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        response = json.dumps(responseBody, indent=4,
                              sort_keys=True, default=str)
        logging.info('Response: ' + response)
        byteStringResponse = response.encode('utf-8')
        self.wfile.write(byteStringResponse)

if __name__ == '__main__':
    hostName = "localhost"
    serverPort = 8084
    appServer = HTTPServer((hostName, serverPort), BaseAppService)
    logging.info('Server started http://%s:%s' % (hostName, serverPort))

    try:
        appServer.serve_forever()
    except KeyboardInterrupt:
        pass

    appServer.server_close()
    logging.info('Server stopped')