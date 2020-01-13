# app.py - a minimal flask api using flask_restful
from flask import Flask
from flask_restplus import Resource, Api
import re, json

app = Flask(__name__)
api = Api(app)

@app.route('/<did>/eidas')
def getQEC(did):
  with open('./data/eidas.json', 'r') as myfile:
    data=myfile.read()

  # parse file
  eidas_data = json.loads(data)
  return json.dumps(eidas_data, indent=2).encode()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="9092")