import logging
import json
import ast
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs
# from generateArt import createPrompt, openAIArtRequest
# from updateTasksInDB import createTask, updateTaskName, updateTaskDay, completeTask, getNumCompletedTasks, clearRecentlyCompletedTasks
from updateTasksInDB import createTask, updateTaskName, updateTaskDay, completeTask, getNumCompletedTasks
# from manageImages import saveBase64Image, cat

logging.basicConfig(level=logging.DEBUG)


class BaseAppService(BaseHTTPRequestHandler):

    HTTP_STATUS_RESPONSE_CODES = {
        'OK': HTTPStatus.OK,
        'FORBIDDEN': HTTPStatus.FORBIDDEN,
        'NOT_FOUND': HTTPStatus.NOT_FOUND,
    }

    # Here's a function to extract GET parameters from a URL
    def extract_GET_parameters(self):
        path = self.path
        parsedPath = urlparse(path)
        paramsDict = parse_qs(parsedPath.query)
        logging.info('GET parameters received: ' + json.dumps(paramsDict, indent=4, sort_keys=True))
        return paramsDict

    def extract_POST_Body(self):
        # The content-length HTTP header is where our POST data will be in the request. So we'll need to
        # read the data using an IO input buffer stream built into the http.server module.
        postBodyLength = int(self.headers['content-length'])
        postBodyString = self.rfile.read(postBodyLength)
        postBodyDict = json.loads(postBodyString)
        logging.info('POST Body received: ' +
                     json.dumps(postBodyDict, indent=4, sort_keys=True))
        return postBodyDict

    ## GET REQUEST HANDLING ##

    def do_GET(self):
        path = self.path
        paramsDict = self.extract_GET_parameters()
        status = self.HTTP_STATUS_RESPONSE_CODES['NOT_FOUND']
        responseBody = {}

        if '/update-task' in path:
            status = self.HTTP_STATUS_RESPONSE_CODES['OK']

            response = "Python service is up and running!"

            responseBody['data'] = response

        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        response = json.dumps(responseBody)
        logging.info('Response: ' + response)
        byteStringResponse = response.encode('utf-8')
        self.wfile.write(byteStringResponse)
    
    def do_POST(self):
        path = self.path
        # Extract the POST body data from the HTTP request, and store it into a Python
        # dictionary we can utilize inside of any of our POST endpoints.
        postBody = self.extract_POST_Body()
        status = self.HTTP_STATUS_RESPONSE_CODES['NOT_FOUND']

        responseBody = {}
        # These path endpoints can be very picky sometimes, and are very much connected to how your DevOps
        # has configured your web server. You will need to communicate with your DevOps to decide on these

        if path == '/':
            status = self.HTTP_STATUS_RESPONSE_CODES['OK']
            responseBody['data'] = 'Hello world'

        # keeping the below here just because NGINX is wierd sometimes and needs a path to match
        #  exactly what's in sites-available
        # elif path == '/update-task': 
        # # we'll include the rest (/update-task/delete, /change-time) later
        # # elif path == 'update-task/update-day': # should be update-task-day

        #     status = self.HTTP_STATUS_RESPONSE_CODES['OK']
            
        #     dataString = json.dumps(postBody)
        #     response = ast.literal_eval(dataString)
        #     # eventually this should be taskUserID
        #     # responseBody = getTasksFromDB(response["taskUser"]) 
        #     # get all tasks from db
        #     # eventually, we'll want to pass taskUser (eventually taskUserID) to get all the tasks that belong to a
        #     #   certain user
        #     # responseBody = getTasksFromDB()
        #     responseBody = "cat"
        
        elif path == '/update-task/create-task':
            status = self.HTTP_STATUS_RESPONSE_CODES['OK']
            dataString = json.dumps(postBody)
            response = ast.literal_eval(dataString)

            # createTask(response["taskUser"]) # should probably be "taskUserID"

            responseBody = createTask(response["taskUser"]) # should probably be "taskUserID"
            # testing shit:
            # createTask("1", "created-task", "testday", "00:00", "00:01")
            # createTask(
            #     response["taskUser"], 
            #     response["taskName"], 
            #     response["taskDay"], 
            #     response["taskStart"], 
            #     response["taskEnd"])
            # responseBody = "/update-task/create-task"

        elif path == '/update-task/update-name':
            status = self.HTTP_STATUS_RESPONSE_CODES['OK']
            dataString = json.dumps(postBody)
            response = ast.literal_eval(dataString)

            updateTaskName(response["taskID"], response["newName"])
            # testing shit:
            # responseBody = "/update-task/update-name"

        elif path == '/update-task/update-day':
            # we'll include the rest (/update-task/delete, /change-time) later
            # should be update-task-day

            # need to take the taskID as a parameter
            # need to update the task day in the database
            # something like: updateTasksInDB("change-day", "new-day")
            status = self.HTTP_STATUS_RESPONSE_CODES['OK']
            dataString = json.dumps(postBody)
            response = ast.literal_eval(dataString)
            
            updateTaskDay(response["taskID"], response["newDay"])
        
        elif path == '/update-task/complete-task':
            # we need to take all of the tasks information here so we can move it all to 
            #  the other database. 
            status = self.HTTP_STATUS_RESPONSE_CODES['OK']
            dataString = json.dumps(postBody)
            response = ast.literal_eval(dataString)
            
            # save taskUser as a variable
            completeTask(
                response["taskID"], 
                response["taskUser"],
                response["taskName"],
                response["taskDay"],
                response["taskStart"],
                response["taskEnd"])
            
            numCompletedTasks = getNumCompletedTasks()
            # responseBody['data'] = numCompletedTasks
            if (numCompletedTasks >= 5): # should be === 5 eventually
                # create a piece of art based on tasks
                # generatedImageBase64 = openAIArtRequest()
                # generate save the art in the droplet
                # saveBase64Image(response["taskID"], generateImageBase64)
                # saveBase64Image("1", generatedImageBase64)
                # responseBody['data'] = cat()
                responseBody['data'] = "fish"
                # clearRecentlyCompletedTasks() # do this when we're done testing
                
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # When using the json.dumps() method, you may encounter data types which aren't easily serializable into
        # a string. When working with these types of data you can include an additional parameters in the dumps()
        # method, 'default=str' to let the serializer know to convert to a string when it encounters a data type
        # it doesn't automatically know how to convert.
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