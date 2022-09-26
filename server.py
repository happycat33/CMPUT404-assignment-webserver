#  coding: utf-8 
import socketserver
import os
from os import path

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
        # The request should be read and need to determine the path of the request so i know which file to return
        # once file is deduce (which will be in www *treat certain paths differently), need to return the data of that file (with the appropriate format)
        # don't worry about returning multiple files (just return html, and computer will also reutrn css automatically)

        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        request = (str(self.data).replace("b'","")).split("\\r\\n")[0]
        request_list = request.split(" ")
        request_path = request_list[1]
        full_path = self.base_path + request_path 

        if request_list[0] == "GET":
            if path.isdir(full_path) and full_path[-1] != '/':
                header = 'HTTP/1.1 301 Moved permanently\r\ncontent-type: text/html\r\nlocation: http://127.0.0.1:8080%s/\r\n' % request_path
                self.response = header

            else:
                if path.isdir(full_path):
                    html_file = None
                    header = 'HTTP/1.1 200 OK\r\ncontent-type: text/html\r\n\r\n'

                    for file in os.listdir(full_path):
                        if file.endswith('.html'):
                            html_file = file

                    with open(full_path + str(html_file), 'r') as f:
                        file = str(f.read())

                    self.response = header + file

                else:
                    if path.exists(full_path):
                        if ".html" in full_path:
                            header = 'HTTP/1.1 200 OK\r\ncontent-type: text/html\r\n\r\n'
                            
                        else:
                            header = 'HTTP/1.1 200 OK\r\ncontent-type: text/css\r\n\r\n'
                        
                        with open(full_path, 'r') as f:
                            file = str(f.read())

                        self.response = header + file 
                    else:
                        self.response = 'HTTP/1.1 404 PAGE NOT FOUND\r\ncontent-type: text/html\r\n\r\n'
        else:
            self.response = 'HTTP/1.1 405 Method Not Allowed\r\ncontent-type: text/html\r\n\r\n'

        self.request.sendall(bytearray(self.response, 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
