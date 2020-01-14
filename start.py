# eidas_start_demo.py
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from api.eidas_bridge_api import init_api_server

if __name__ == "__main__":  
  init_api_server()