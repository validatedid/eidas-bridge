import http.server
import socketserver

DIRECTORY = "demo/university_backend"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_backend_server(host='0.0.0.0', port='8080'):
    try:
        with socketserver.TCPServer((host, port), Handler) as httpd:
            print(' * Starting web backend server at http://' + host + ':' + str(port))
            httpd.serve_forever()
    except KeyboardInterrupt:
        print (" * Exiting web backend server")