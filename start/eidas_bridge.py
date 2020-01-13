# eidas_start_demo.py
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import argparse, multiprocessing, time
multiprocessing.set_start_method('spawn', True)
from demo.util.hub_server import start_hub_server
from start.eidas_bridge_api import init_api_server

def main(args):

    # Start the job processes
    try:
        hub_server_proc = multiprocessing.Process(target=start_hub_server)
        api_server_proc = multiprocessing.Process(target=init_api_server, args=(args.host, args.apiport,))

        # launch servers
        hub_server_proc.start()
        api_server_proc.start()

        # Keep the main thread running, otherwise signals are ignored.
        while True:
            time.sleep(0.5)
 
    except KeyboardInterrupt:
        # Terminate the running processes.
        hub_server_proc.terminate()
        api_server_proc.terminate()
        print('\n * Exiting eIDAS Bridge server')

if __name__ == "__main__":
    
    print (" * Starting eIDAS Bridge demo")
    parser = argparse.ArgumentParser(description="Runs an eIDAS Bridge server")
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

    args = parser.parse_args()

    main(args)