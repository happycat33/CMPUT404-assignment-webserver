#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Copyright 2022 Kimberly Tran
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    base_path = 'www'
    response = None

    def handle(self):
        # When we first receive the request, we split it into its different components, and grab the specific request method (GET, PUT, etc.). We then
        # check if the path given includes "/.." (which means directory traversal attack) and we remove them. We then add the base path (which is www/) 
        # and add them together. Then we check the method, if its GET, we continue, else we return 405. All checks will return a appropriate header and,
        # at the end, we return that response

        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        request = (str(self.data).replace("b'","")).split("\\r\\n")[0]
        request_list = request.split(" ")
        request_path = request_list[1]
        
        # While code not given, rmo1 suggested something similar to solve directory traversal attack
        
        if("/.." in request_path):
            request_path = request_path.strip("/..")
        full_path = self.base_path + request_path

        if request_list[0] == "GET":
            if os.path.isdir(full_path) and full_path[-1] != '/':
                # Here we check if the path given is a directory, if so we check if the request path ends with "/", if not, we redirect the request to
                # one with "/" at the end.

                header = 'HTTP/1.1 301 Moved permanently\r\ncontent-type: text/html\r\nlocation: http://127.0.0.1:8080%s/\r\n' % request_path
                self.response = header

            else:
                # If the path given is a directory, then we return the appropriate header and then search that directory for the html file we need 
                # (in most cases, it is "index.html"). then we attach that file to the end of the path and open the file and read it, we then attach
                # the string version of the file to the header and return the response. However, if there is an issue with the directory (such as no
                # files existing in the directory), we returna 404 error. 

                if os.path.isdir(full_path):
                    html_file = None
                    header = 'HTTP/1.1 200 OK\r\ncontent-type: text/html\r\n\r\n'

                    for file in os.listdir(full_path):
                        if file.endswith('.html'):
                            html_file = file
                    try:
                        with open(full_path + str(html_file), 'r') as f:
                            file = str(f.read())

                        self.response = header + file

                    except:
                        self.response = 'HTTP/1.1 404 PAGE NOT FOUND\r\n\r\n'

                else:
                    # If the path given is not a directory, we assume we are given a file path. We then check if the file path exists in ww/. If so,
                    # then we check if we're given a html or css file and return the appropriate mime type and header". Then similar to the previous if
                    # statement, we open the file path, read it and attach the string version to the header and return the response.

                    if os.path.exists(full_path):
                        file_name = full_path.split('/')[-1]

                        if ".html" in file_name:
                            header = 'HTTP/1.1 200 OK\r\ncontent-type: text/html\r\n\r\n'
                            
                        else:
                            header = 'HTTP/1.1 200 OK\r\ncontent-type: text/css\r\n\r\n'

                        with open(full_path, 'r') as f:
                            file = str(f.read())

                        self.response = header + file 

                    else:

                        # if the path is not a directory and the file doesn't exists, we return a 404 response

                        self.response = 'HTTP/1.1 404 PAGE NOT FOUND\r\n\r\n'
        else:
            self.response = 'HTTP/1.1 405 Method Not Allowed\r\n\r\n'

        self.request.sendall(bytearray(self.response, 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
