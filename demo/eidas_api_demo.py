# eidas_api_demo.py
""" RESTFUL API for EIDAS BRIDGE DEMO """

import json, threading
from flask import Flask, request
from flask_restplus import Resource, Api
from flask_jsonpify import jsonify
from eidas_demo import demo_eidas_link_did, demo_eidas_get_service_endpoint, \
    demo_eidas_sign_credential, demo_eidas_verify_credential
from util.hub_server import start_hub_server

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

name_space = api.namespace('eidas', description="eIDAS DEMO APIs")

@name_space.route('/link-did')
class EIDASLinkDID(Resource):
    def get(self):
        """ 
        Link the Issuer DID with eIDAS certificate

        Receives a DID, an eIDAS certificate, its proof of possession, and 
        optionally the padding of the signature proof (accepts PKCS#1 and PSS)

        Returns the JSON that needs to be stored on the Agent public Storage
        (i.e: an Identity Hub)
        """
        return jsonify(json.loads(demo_eidas_link_did()))

@name_space.route('/service-endpoint')
class EIDASServiceEndpoint(Resource):
    def get(self):
        """ 
        Contructs the JSON structure that needs to be added to the Issuer's 
        DID Document Service Endpoint Section. 

        Receives a did and a service endpoint where it is stored the issuer's 
        eIDAS and DID linking information.

        Returns the correspondent JSON to be added to the Service Endpoint 
        Section of the Issuer's DID Document.
        """
        return jsonify(json.loads(demo_eidas_get_service_endpoint()))

@name_space.route('/sign-credential')
class EIDASSignCredential(Resource):
    def get(self):
        """ 
        Checks the validity of the issuer's eIDAS certificate against a 
        Trusted Service Provider and adds the corresponde response to the 
        received credential JSON structure.

        Not Supported at this Phase 0.
        """
        return jsonify(demo_eidas_sign_credential())

@name_space.route('/verify-credential')
class EIDASVerifyCredential(Resource):
    def get(self):
        """
        Verifies that the credential issuer had a valid eIDAS certificate 
        at the moment of issuing the passed credential.

        Throws EIDASProofException on signarure not valid
        """
        server_thread = threading.Thread(target=start_hub_server, daemon=True)

        # launch localhost server
        server_thread.start()
        # check if server started
        if server_thread.is_alive():
            return jsonify(demo_eidas_verify_credential())
        else:
            return "ERROR: Cannot start server"

if __name__ == '__main__':
     app.run(port='5002')