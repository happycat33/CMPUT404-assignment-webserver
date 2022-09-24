#  coding: utf-8 
import socketserver

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
    
    root_path = 'www/index.html'
    root_css = 'www/base.css'
    deep_path = 'www/deep/index.html'
    deep_css = 'www/deep/deep.css'
    response = None

    def handle(self):
        # The request should be read and need to determine the path of the request so i know which file to return
        # once file is deduce (which will be in www *treat certain paths differently), need to return the data of that file (with the appropriate format)
        # don't worry about returning multiple files (just return html, and computer will also reutrn css automatically)

        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        request = (str(self.data).replace("b'","")).split("\\r\\n")[0]
        request_list = request.split(" ")
        if request_list[0] == "GET":
            if request_list[1] == '/deep':
                header = 'HTTP/1.1 301 Moved permanently\r\ncontent-type: text/html\r\nlocation: http://127.0.0.1:8080%s/\r\n' %request_list[1]
                self.response = header
            else:
                if request_list[1] == '/' or request_list[1] == '/hardcode/' or request_list[1] == "/hardcode/index.html" or request_list[1] == '/index.html':
                    with open(self.root_path, 'r') as f:
                        file = str(f.read())
                    header = 'HTTP/1.1 200 OK\r\ncontent-type: text/html\r\n\r\n' 
                    self.response = header + file
                elif request_list[1] == '/base.css':
                    with open(self.root_css, 'r') as f:
                        file = str(f.read())
                    header = 'HTTP/1.1 200 OK\r\ncontent-type: text/css\r\n\r\n'
                    self.response = header + file
                elif request_list[1] == '/deep/' or request_list[1] == '/deep/index.html':
                    with open(self.deep_path, 'r') as f:
                        file = str(f.read())
                    header = 'HTTP/1.1 200 OK\r\ncontent-type: text/html\r\n\r\n'
                    self.response = header + file
                elif request_list[1] == '/deep/deep.css' or request_list[1] == '/deep/index.html/deep.css':
                    with open(self.deep_css, 'r') as f:
                        file = str(f.read())
                    header = 'HTTP/1.1 200 OK\r\ncontent-type: text/css\r\n\r\n'
                    self.response = header + file
                else:
                    self.response = 'HTTP/1.1 404 Page Not Found\r\ncontent-type: text/html\r\n\r\n'
        else:
            header = 'HTTP/1.1 405 Method Not Allowed\r\ncontent-type: text/html\r\n\r\n'
            self.response = header + "NO GOOD!"

        self.request.sendall(bytearray(self.response, 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
