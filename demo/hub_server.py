# eidas_start_demo.py
from flask import Flask
from flask_restplus import Resource, Api
import re, json

app = Flask(__name__)
api = Api(app)

@app.route('/')
def getC():
  print('I\'m in!!')

@app.route('/<did>/eidas')
def getQEC(did):
  try:
    with open('./data/eidas.json', 'r') as myfile:
      data=myfile.read()
  except FileNotFoundError:
    with open('./demo/data/eidas.json', 'r') as myfile:
      data=myfile.read()
  return json.loads(data)
  # parse file
  # eidas_data = json.loads(data)
  # return json.dumps(eidas_data, indent=2).encode()


def init_hub_server(host='0.0.0.0', port='9001'):
  # run api demo
  print(' * Starting API server at http://'+host+':'+ str(port))
  app.run(host, port)

if __name__ == '__main__':
  init_hub_server()