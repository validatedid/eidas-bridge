import http.server
import socketserver
import os

DIRECTORY = "../university_backend/"

web_dir = os.path.join(os.path.dirname(__file__), DIRECTORY)
os.chdir(web_dir)

def start_backend_server(host='0.0.0.0', port=8080):
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer((host, port), Handler)
    print(' * Starting web backend server at http://' + host + ':' + str(port))
    httpd.serve_forever()