from datetime import datetime

import http.server
import socketserver
import json


PORT = 8080


#Handler = http.server.SimpleHTTPRequestHandler
class Handler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def do_HEAD(self):
        self._set_headers()
        
    # GET sends back a Hello world message
    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps({'now': datetime.now().isoformat()}).encode())


with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()

