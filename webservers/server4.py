#!/usr/bin/env python
"""
https://gist.github.com/bradmontgomery/2219997

Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost:8000/data=10
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import os
import random

# Generate a series of n numbers
# by adding random -1, +1 to an
# initial value
def generate(n, initial_value):
    x = initial_value
    output = [x]
    for i in range(0,n):
        x = x + 2*random.randint(0,1) - 1
        output.append(x)
    return output


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        print self.path
        if self.path.find("/data=") == 0:
            [prefix,arg] = self.path.split("=")
            print "arg = " + arg
            message = generate(int(arg), 0)
            print message
        else:
            message = "I don't understand"
        self._set_headers()
        self.wfile.write(message)

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
