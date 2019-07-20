# eidas_bridge_api.py
""" RESTFUL API for EIDAS BRIDGE """

import json, threading
from flask import Flask, request
from flask_restplus import Resource, Api, fields
from flask_jsonpify import jsonify
from eidas_demo import init_server
from eidas_bridge.eidas_bridge import eidas_link_did, eidas_get_service_endpoint, \
    eidas_sign_credential, eidas_verify_credential, EIDASNotSupportedException
from eidas_bridge.utils.crypto import PSS_PADDING
from data.common_data import eidas_link_inputs, service_endpoints, credentials, paddings, \
    did_documents

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app, version='1.0', title='eIDAS Bridge API', description='An eIDAS bridge API to connect to a SSI solution')

eidas = api.namespace('eidas', description="eIDAS bridge API calls")

eidas_link_input_model = api.model('EIDASLink_in', {
    'did': fields.String(description="DID", required=True),
    'certificate': fields.String(description="x509 certificate", required=True),
    'proof': fields.String(description="DID-hashed signature with public key", required=True),
    'padding': fields.String(description="Signature padding: PKCS1-v1_5 or PSS. Default = PSS", default=PSS_PADDING)
})

proof_model = api.model('EIDAS_proof', {
    'type' : fields.String(description="Signature type", required=True),
    'padding': fields.String(description="Signature padding: PKCS1-v1_5 or PSS", required=True),
    'signatureValue' : fields.Raw(description="DID-hashed signature with public key", required=True)
})

eidas_link_output_model = api.model('EIDASLink_out', {
    'type': fields.String(description="Structure type: should be EidasLink", required=True),
    'created': fields.String(description="Structure datetime stamp creation: should be similar to '2002-10-10T17:00:00Z'", required=True),
    'did': fields.String(description="DID", required=True),
    'certificate': fields.Raw(description="x509 certificate", required=True),
    'proof': fields.Nested(proof_model, description="Signature proof structure", required=True)
})


@eidas.route('/link-did')
class EIDASLinkDID(Resource):
    @eidas.marshal_with(eidas_link_output_model)
    @eidas.expect(eidas_link_input_model)
    def post(self):
        """ 
        Link the Issuer DID with eIDAS certificate

        Receives a DID, an eIDAS certificate, its proof of possession, and 
        optionally the padding of the signature proof (accepts PKCS#1 and PSS)

        Returns the JSON that needs to be stored on the Agent public Storage
        (i.e: an Identity Hub)
        """
        output = eidas_link_did(
                request.json['did'], 
                (request.json['certificate']).encode(), 
                bytes.fromhex(request.json['proof']), 
                request.json['padding']
            )
        return json.loads(output)

@eidas.route('/service-endpoint')
class EIDASServiceEndpoint(Resource):
    def get(self):
        """ 
        Contructs the JSON structure that needs to be added to the Issuer's DID Document Service Endpoint Section. 

        Receives a did and a service endpoint where it is stored the issuer's 
        eIDAS and DID linking information.

        Returns the correspondent JSON to be added to the Service Endpoint 
        Section of the Issuer's DID Document.
        """

        output = eidas_get_service_endpoint(
                service_endpoints[0][0], 
                service_endpoints[0][1]
            )
        return jsonify(json.loads(output))

@eidas.route('/sign-credential')
class EIDASSignCredential(Resource):
    def get(self):
        """ 
        Checks the validity of the issuer's eIDAS certificate against a Trusted Service Provider and adds the corresponde response to the received credential JSON structure.

        Not Supported at this Phase 0.
        """
        try:
            return eidas_sign_credential(credentials[0])
        except EIDASNotSupportedException:
            return "--- EIDAS Library function NOT supported yet. ---"

@eidas.route('/verify-credential')
class EIDASVerifyCredential(Resource):
    def get(self):
        """
        Verifies that the credential issuer had a valid eIDAS certificate at the moment of issuing the passed credential.

        Return "VALID" or Throws EIDASProofException on signarure not valid
        """
        server_thread = threading.Thread(target=init_server, daemon=True)

        # launch localhost server
        server_thread.start()
        # check if server started
        if server_thread.is_alive():
            return eidas_verify_credential(
                    json.dumps(credentials[0]), 
                    json.dumps(did_documents[0])
            )
        else:
            return "ERROR: Cannot start server"

if __name__ == '__main__':
     app.run(port='5002')