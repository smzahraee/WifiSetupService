
import http.server as server
import ssl
import os
import logging
import json
from threading import Thread
from urllib.parse import urlparse
import cgi


class HttpRequestHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.check_not_found():
            return
        content="Functionland hotspot connected"
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content.encode("ascii"))

    def do_POST(self):
        if self.check_not_found():
            return
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        json_str = json.dumps({'hello': 'world', 'received': 'ok'})
        self.wfile.write(json_str.encode(encoding='utf_8'))
        return
    
    def check_not_found(self):
        if self.path != "/":
                self.send_response(404)
                content = "Not Found"
                self.send_header("Content-Type", "text/plain")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content.encode("utf_8"))
                return True
        return False


class RedirectHttptoHttps(server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(301)
        self.send_header('Location','https://localhost:4443')
        self.end_headers()
        return

def run_redirect_server():
    server_address = ('localhost', 80)
    httpd = server.HTTPServer(server_address, RedirectHttptoHttps)
    httpd.serve_forever()

def run_web_api():
    logging.debug("Start https server...")

    server_address = ('localhost', 4443)

    httpd = server.HTTPServer(
        server_address, HttpRequestHandler)
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   server_side=True,
                                   certfile='mycert.pem',
                                   ssl_version=ssl.PROTOCOL_TLS)
    httpd.serve_forever()
