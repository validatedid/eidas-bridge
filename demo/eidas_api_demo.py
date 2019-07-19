# eidas_api_demo.py
""" RESTFUL API for EIDAS BRIDGE DEMO """

import json, threading
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from eidas_demo import init_server, demo_eidas_link_did, demo_eidas_get_service_endpoint, \
    demo_eidas_sign_credential, demo_eidas_verify_credential

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

@app.route('/eidas/link-did', methods=['GET'])
def get_eidas_link_did():
    return jsonify(json.loads(demo_eidas_link_did()))

@app.route('/eidas/service-endpoint', methods=['GET'])
def get_eidas_service_endpoint():
    return jsonify(json.loads(demo_eidas_get_service_endpoint()))

@app.route('/eidas/sign-credential', methods=['GET'])
def get_eidas_sign_credential():
    return jsonify(demo_eidas_sign_credential())

@app.route('/eidas/verify-credential', methods=['GET'])
def get_eidas_verify_credential():
    server_thread = threading.Thread(target=init_server, daemon=True)

    # launch localhost server
    server_thread.start()
    # check if server started
    if server_thread.is_alive():
        return jsonify(demo_eidas_verify_credential())
    else:
        return "ERROR: Cannot start server"

if __name__ == '__main__':
     app.run(port='5002')