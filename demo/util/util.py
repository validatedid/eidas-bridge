# util.py
""" data and functions to better testing """

import threading
from .server import start_server

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_object(input_obj):
    print("{}".format(input_obj.decode()))

class LocalServer():
    
    def __init__(self):
        self.server_started = False

    def start_server_localhost(self):
        """ Start localhost server to retrieve EIDAS LINK DID structure """
        if not self.server_started:
            self.server_started = True
            start_server()

def _init_server():
    server = LocalServer()
    server.start_server_localhost()

def start_server_thread() -> bool:
    server_thread = threading.Thread(target=_init_server, daemon=True)
    
    # launch localhost server
    server_thread.start()
    # check if server started
    if server_thread.is_alive():
        return True
    else:
        return False
