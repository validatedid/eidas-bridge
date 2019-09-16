from http.server import BaseHTTPRequestHandler, HTTPServer
import re, json

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if None != re.search('/*/eidas', self.path):
            # read file
            with open('./demo/data/eidas.json', 'r') as myfile:
                data=myfile.read()

            # parse file
            eidas_data = json.loads(data)

            # print values
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(eidas_data, indent=2).encode())
        return

def start_hub_server():
    server = HTTPServer(('localhost', 8001), RequestHandler)
    print(' * Starting Hub server at http://localhost:8001')
    server.serve_forever()