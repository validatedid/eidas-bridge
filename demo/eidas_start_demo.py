# eidas_start_demo.py
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import threading, signal, argparse
from demo.util.hub_server import start_hub_server
from demo.util.backend_server import start_backend_server
from demo.eidas_bridge_api import init_api_server

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Runs an eIDAS Bridge demo with a University backend web")
    parser.add_argument(
        "-host",
        "--host",
        type=str,
        default='0.0.0.0',
        metavar=("<ip host>"),
        help="Choose the starting ip host to point to your server",
    )
    parser.add_argument(
        "-p",
        "--apiport",
        type=int,
        default=5002,
        metavar=("<API Swagger port>"),
        help="Choose the starting port number to listen on from the API SWAGGER",
    )
    parser.add_argument(
        "-p1",
        "--webport",
        type=int,
        default=8080,
        metavar=("<Demo web port>"),
        help="Choose the starting port number to listen on to the demo backend web",
    )

    args = parser.parse_args()

    hub_server_thread = threading.Thread(target=start_hub_server, daemon=True)
    api_server_thread = threading.Thread(target=init_api_server, args=(args.host, args.apiport,),)
    web_demo_server_thread = threading.Thread(target=start_backend_server, args=(args.host, args.webport,),)

    print (" * Starting eIDAS Bridge demo")
    # launch hub server
    hub_server_thread.start()
    # check if server started
    if hub_server_thread.is_alive():
        # launch api server
        web_demo_server_thread.start()
        if web_demo_server_thread.is_alive():
            # launch api server
            api_server_thread.start()