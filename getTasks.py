import logging
import json
import ast
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs
from getInfoFromDB import getTasksFromDB
from updateTasksInDB import getNumCompletedTasks

logging.basicConfig(level=logging.DEBUG)

# this service returns an object of tasks and the number of completed tasks
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

        # returns a dictionary of all tasks in the db
        elif path == '/get-tasks':
            status = self.HTTP_STATUS_RESPONSE_CODES['OK']
            dataString = json.dumps(postBody)
            response = ast.literal_eval(dataString)
            # eventually this should use the ID of a given user to retrieve their tasks (not just all tasks)
            responseBody = getTasksFromDB()

        # returns a string that represents the # of completed tasks
        elif path == '/get-tasks/get-num-completed':
            status = self.HTTP_STATUS_RESPONSE_CODES['OK']
            dataString = json.dumps(postBody)
            response = ast.literal_eval(dataString)
            # eventually this should use the ID of a given user to retrieve the number of their completed
            #   tasks (not just all completed tasks)
            responseBody['numCompletedTasks'] = getNumCompletedTasks()
        
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
    serverPort = 8083
    appServer = HTTPServer((hostName, serverPort), BaseAppService)
    logging.info('Server started http://%s:%s' % (hostName, serverPort))

    try:
        appServer.serve_forever()
    except KeyboardInterrupt:
        pass

    appServer.server_close()
    logging.info('Server stopped')