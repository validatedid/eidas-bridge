# eidas_bridge_api.py
""" RESTFUL API for EIDAS BRIDGE """

import json, threading
from flask import Flask, request
from flask_restplus import Resource, Api, fields
from demo.util.hub_server import start_hub_server
from eidas_bridge.eidas_bridge import eidas_get_service_endpoint, \
    eidas_sign_credential, eidas_verify_credential, EIDASNotSupportedException, \
    eidas_load_qec, eidas_get_pubkey
from eidas_bridge.utils.crypto import PSS_PADDING

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app, version='0.5', title='eIDAS Bridge API', description='An eIDAS bridge API to connect to a SSI solution')

eidas = api.namespace('eidas', description="eIDAS bridge API calls")

eidas_load_qec_input_model = api.model('EIDASLoadQEC', {
    'did': fields.String(
        description="DID", 
        required=True,
        example="did:example:21tDAKCERh95uGgKbJNHYp"),
    'p12data': fields.Raw(
        description="QEC certificate with Secp256k1 keys in a P12 format", 
        required=True,
        example=(b'0\x82\x03\xc9\x02\x01\x030\x82\x03\x8f\x06\t*\x86H\x86\xf7\r\x01\x07\x01\xa0\x82\x03\x80\x04\x82\x03|0\x82\x03x0\x82\x02w\x06\t*\x86H\x86\xf7\r\x01\x07\x06\xa0\x82\x02h0\x82\x02d\x02\x01\x000\x82\x02]\x06\t*\x86H\x86\xf7\r\x01\x07\x010\x1c\x06\n*\x86H\x86\xf7\r\x01\x0c\x01\x060\x0e\x04\x08\'?\xfc\xa4]\xbf\x80k\x02\x02\x08\x00\x80\x82\x020}A9N;\x89/j\x8e8\xc57=\x1d!\xae!0\xcd\xaf7}cN>\xcac\xb6nqU\x8c>\x1ff\xce\xe45\xcf\r\xb8~O\xf1\xae\xd5\xde \x0ch\xe1\xe3]\x90\xbc\xa5cBv\xbc\xbf\xc3\x1a\xf2\x91\xa6\x9a\xd1\xac"?\xealH\x06\xf0\xce\xb8\x96s\xc7\xca\x0bK\xaa\xe7+\xa5\xe3\xb7\x82\x07\xfc\x1d%<\x95\x9d:\xff\xed\xc7\x03\xb9\x7f\xa5\xbb\xab\xfd`\x17\x01\x1fp\xe6W\xc7\x88\xde\xa4\xa7\xd2\x8f\xb48m[\xcdl\xb6\xba#0B\x97\xae[\x8d\xf4\x99\xa4\xcb\x94\xea>\x04\xbc\xc7\'\xc2\xc4\xc0b\x01\xe7\xb6O\xfe\xdaA~\xb7\xa8\x8a\x02\x82\x7f\xe9\x1f\xae\x8c\xef=\xf6\x90(\xddK\xe5\xeaB$XC\x84U\\N=ut\xc9\xe5]\xe2\x0b\xe8\x80\xc3\x84G~M\xa8+\xb1\xb0sL\xcb\xb7&\xb4jQM\x8c\x8c\x8b\xbe\xbe7Zghj\x1b\xf5\x00\xe1\x06f.\xbb\xf5\x98\xf8j$\xa2\xc9L\xe1\x08S\xbe\xc2Z\x14f\xb6\xa3\xa2\x8dI\xd1\x07~\x08\x9e\xdf\xd2"\xc9\xaa\xc8a\xc5Q\x89\xac\x91{\x967H]c0\xa2N\xe4\xbe\x14\x18\xe3aC\x88B\x80\r\x84\x90\xcf\xf8\x9c2\xccs\xea~bg\x99OU\x04WU:\xc9\x03\x9e\xfa\x96\x13D\x89}\xed\x92\xc5?G\xf7\xdb\xa3\x0eg;\x01\x93-\x88\xa5;\xc6\xc1:\xe3\x93\xfa\x9a9\xde\xe5:\\\x88\x8a\x92\xf9T\xb4|\xa4\xf3\xecT-\xc0\xa7Y\xf3\x0f\x0c\xb3\x92\x06\t\x9f\x1c\x96\x9c\xf4*\xfc.\x1b7.\xa2\x80\x1b\xd2\xf8DQ\xa4\x86\x13\x16E\x1b%\x90%\xeaO\xf0#\x06\x87\xe0\x8a\xfe\xcc\xb0\xb6F\x08\xb1y\xca\xc8\x92\x0bD\xd6\xd0\xb2\xfd\xa4[[\xe3\xcf\xe2\x9c\x00\x97\xbc\x95\x0f\x8a\xaf\xbb\x8c\xa6\xaa]5\xb3\x01[\xc1a\xe9\x06@\x8a\xbc\xd8]\xba\'&\xd6\xaa_\x9e+c\xfb\x9d\xc6\xbc\xd8\x1d\xe5t\xe8\x9eL@\x80\x99\xeeV\x12\x06\x04a\xaa7J\xbd\xa1\xe3p2_\x9b\xd7\xb6\xdd\x98\xf1kx\x19\x9a\xc8\xdeXP\xa6\x15\xd7\xb5\xc9\xb1N\xefbZ\xb6\x8e\x91\xff\xa2\x877\x84f\xc1\xee\xcd7\x1dZp\xc4\xce\xe3\x1f\xda\x0e\x9fY\xa3\xce\x0b~N\xaa\xe6\x91\xee<\xf0\x13\xa1:\x1a\x0f\xdf\xce%0\x81\xfa\x06\t*\x86H\x86\xf7\r\x01\x07\x01\xa0\x81\xec\x04\x81\xe90\x81\xe60\x81\xe3\x06\x0b*\x86H\x86\xf7\r\x01\x0c\n\x01\x02\xa0\x81\xac0\x81\xa90\x1c\x06\n*\x86H\x86\xf7\r\x01\x0c\x01\x030\x0e\x04\x08\xfa\xe77\x12\xfb\xcbB\xe9\x02\x02\x08\x00\x04\x81\x88(\xde\x9f?\xc3\xcc#f\xb9>\x12\xa1\xd7\xefF\xea\xa3\xd8\x88v%\x1cv\xf8I\xb4K\x1e\xc6q\x85\xe2\x95a\x83*pI@\x13q\x19>\xdb\xce\xb0\x86 \x16n\xce\xc1\xe0cl\xd7_H\xc2\x8c\xac\xdc\xc5<\xb58\xe6\xfa\xfc\xf8\xf5HRH\x83\x17\xd5(\xcf;=z\x12r\x18z\x95\x7fz\xb4\xac\xeb0\xe8\xc4\xb5O\xae>\xa07C>,\xd2\xd3;\xbeQ\xab\xdc\xb0\x01\xd8\x93s\xfchu\xae\xbe\x97%\x19\xb5\xf4\xbc\xb9\x05\x83\xcc)/\xbc\x16e1%0#\x06\t*\x86H\x86\xf7\r\x01\t\x151\x16\x04\x14]F\x8e\xb5\xcd\x8c\r\xb1q\xcd\xf3\x87X\x80\x9f\x04\xac\x95\xeb\xc8010!0\t\x06\x05+\x0e\x03\x02\x1a\x05\x00\x04\x14\x13m\x9f\xe5m\x93^\xb5G\x81q\xf4\x1aN\xf2\x90\xdeb\xb06\x04\x08\xf9\x10\x1c\x1c:f\xca\xb7\x02\x02\x08\x00').hex()),
    'password': fields.String(
        description="DID-hashed signature with public key", 
        required=True,
        example="passphrase")
})

@eidas.route('/load-qec')
class EIDASLoadQEC(Resource):
    @eidas.expect(eidas_load_qec_input_model)
    def post(self):
        """ 
        Imports an eIDAS Qualified Electronic Certificate (QEC) with its correspondent private key to be used in further digital signature operations.

        QEC currently supported format is only Secp256k1.
        """
        eidas_load_qec(
            request.json['did'], 
            request.json['p12data'], 
            request.json['password']
        )

        return "eIDAS certificate and keys successfully loaded."

eidas_service_input_model = api.model('EIDASService_in', {
    'did': fields.String(
        description="DID", 
        required=True,
        example="did:example:21tDAKCERh95uGgKbJNHYp"),
    'service_endpoint': fields.String(
        description="Service Endpoint", 
        required=True,
        example="http://service_endpoint.sample/did:example:21tDAKCERh95uGgKbJNHYp/eidas")
})

service_output_model = api.model('ServiceEndpoint', {
    'id': fields.String(
        description="Service Endpoint Identifier", 
        required=True,
        example="did:example:21tDAKCERh95uGgKbJNHYp#eidas"),
    'type': fields.String(
        description="Service Endpoint type", 
        required=True,
        example="EidasService"),
    'serviceEndpoint': fields.String(
        description="Service Endpoint URL", 
        required=True,
        example="http://localhost:8000/did:example:21tDAKCERh95uGgKbJNHYp/eidas"),
})

@eidas.route('/service-endpoint')
class EIDASServiceEndpoint(Resource):
    @eidas.marshal_with(service_output_model)
    @eidas.expect(eidas_service_input_model)
    def post(self):
        """ 
        Contructs the JSON structure that needs to be added to the Issuer's DID Document Service Endpoint Section. 

        Receives a did and a service endpoint where it is stored the issuer's 
        eIDAS and DID linking information.

        Returns the correspondent JSON to be added to the Service Endpoint 
        Section of the Issuer's DID Document.
        """

        return json.loads(
            eidas_get_service_endpoint(
                request.json['did'], 
                request.json['service_endpoint']
            )
        )

eidas_get_pubkey_input_model = api.model('EIDASPubKey_in', {
    'did': fields.String(
        description="DID", 
        required=True,
        example="did:example:21tDAKCERh95uGgKbJNHYp")
})

eidas_get_pubkey_output_model = api.model('EIDASPubKey_out', {
    'did': fields.String(
        description="eIDAS Secp256k1 Public key", 
        required=True,
        example="-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE07FtD4Qg4Dw7GKxCUCPAxHN0E5aHahkL\nyE2GCbSRohqUzpVODaIwPaEW5PPNlMtSkODTKVdviyTHP6nY/HJ6Gw==\n-----END PUBLIC KEY-----\n")
})

@eidas.route('/get-pubkey')
class EIDASGetPubKey(Resource):
    @eidas.marshal_with(eidas_get_pubkey_output_model)
    @eidas.expect(eidas_get_pubkey_input_model)
    def get(self):
        """ 
        From a given DID, returns the correspondent public key.

        Cryptographic keys currently supported format are only Secp256k1.
        """

        return json.loads(
            eidas_get_pubkey(
                request.json['did']
            )
        )

degree_model = api.model('Degree', {
    'type' : fields.String(
        description="Credential Degree type", 
        required=True,
        example="BachelorDegree"),
    'name' : fields.String(
        description="Degree name", 
        required=True,
        example="Bachelor of Science and Arts")
})

cred_subject_model = api.model('Credential_subject', {
    'did': fields.String(
        description="DID", 
        required=True,
        example="did:example:21tDAKCERh95uGgKbJNHYp"),
    'degree': fields.Nested(
        degree_model, 
        description="Degree Credential structure", 
        required=True)
})

cred_proof_model = api.model('Credential_proof', {
    'type' : fields.String(
        description="Signature type", 
        required=True,
        example="RsaSignature2018"),
    'created': fields.String(
        description="Credential Issuance date timestamp", 
        required=False,
        example="2018-06-18T21:19:10Z"),
    'proofPurpose': fields.String(
        description="Proof of Purpose", 
        required=False,
        example="assertionMethod"),
    'verificationMethod': fields.String(
        description="Verification Method", 
        required=False,
        example="https://example.com/jdoe/keys/1"),
    'jws' : fields.String(
        description="Proof Value", 
        required=True,
        example="eyJhbGciOiJQUzI1NiIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il19DJBMvvFAIC00nSGB6Tn0XKbbF9XrsaJZREWvR2aONYTQQxnyXirtXnlewJMBBn2h9hfcGZrvnC1b6PgWmukzFJ1IiH1dWgnDIS81BH-IxXnPkbuYDeySorc4QU9MJxdVkY5EL4HYbcIfwKj6X4LBQ2_ZHZIu1jdqLcRZqHcsDF5KKylKc1THn5VRWy5WhYg_gBnyWny8E6Qkrze53MR7OuAmmNJ1m1nN8SxDrG6a08L78J0-Fbas5OjAQz3c17GY8mVuDPOBIOVjMEghBlgl3nOi1ysxbRGhHLEK4s0KKbeRogZdgt1DkQxDFxxn41QWDw_mmMCjs9qxg0zcZzqEJw")
})

credential_input_model = api.model('Credential_in', {
    '@context': fields.List(fields.String,
        description="List of context attributes", 
        required=True,
        example='[ "https://www.w3.org/2018/credentials/v1", "https://www.w3.org/2018/credentials/examples/v1" ]'),
    'id': fields.String(
        description="Credential IDentifier", 
        required=True,
        example="http://example.edu/credentials/3732"),
    'type': fields.List(fields.String,
        description="List of credential types", 
        required=True,
        example='["VerifiableCredential", "UniversityDegreeCredential"]'),
    'issuer': fields.String(
        description="Issuer DID", 
        required=True,
        example="did:example:21tDAKCERh95uGgKbJNHY"),
    'issuanceDate': fields.String(
        description="Credential Issuance date timestamp", 
        required=False,
        example="2010-01-01T19:23:24Z"),
    'credentialSubject': fields.Nested(
        cred_subject_model, 
        description="Credential Subject structure", 
        required=True),
    'proof': fields.Nested(
        cred_proof_model, 
        description="Credential proof structure", 
        required=True)
})

credential_output_model = api.model('Credential_out', {
    '@context': fields.List(fields.String,
        description="List of context attributes", 
        required=True,
        example='[ "https://www.w3.org/2018/credentials/v1", "https://www.w3.org/2018/credentials/examples/v1" ]'),
    'id': fields.String(
        description="Credential IDentifier", 
        required=True,
        example="http://example.edu/credentials/3732"),
    'type': fields.List(fields.String,
        description="List of credential types", 
        required=True,
        example='["VerifiableCredential", "UniversityDegreeCredential"]'),
    'issuer': fields.String(
        description="Issuer DID", 
        required=True,
        example="did:example:21tDAKCERh95uGgKbJNHY"),
    'issuanceDate': fields.String(
        description="Credential Issuance date timestamp", 
        required=False,
        example="2010-01-01T19:23:24Z"),
    'credentialSubject': fields.Nested(
        cred_subject_model, 
        description="Credential Subject structure", 
        required=True),
    'proof': fields.Nested(
        cred_proof_model, 
        description="Credential proof structure", 
        required=True)
})

@eidas.route('/sign-credential')
class EIDASSignCredential(Resource):
    @eidas.marshal_with(credential_output_model)
    @eidas.expect(credential_input_model)
    def post(self):
        """ 
        Adds a digital signature to the given credential, generated with an eIDAS private key.

        Returns the correspondent Verifiable Credential.

        Cryptographic keys currently supported format are only Secp256k1.
        """
        return json.loads(
            eidas_sign_credential(request.get_json())
        )

auth_diddoc_model = api.model('AuthenticationDIDDocModel', {
    'id': fields.String(
        description="Authentication Identifier Key", 
        required=True,
        example="did:example:21tDAKCERh95uGgKbJNHY#keys-1"),
    'type': fields.String(
        description="Authentication Identifier Key type", 
        required=True,
        example="RsaVerificationKey2018"),
    'controller': fields.String(
        description="Owner of Identifier Key", 
        required=True,
        example="did:example:21tDAKCERh95uGgKbJNHY"),
    'publicKeyPem': fields.String(
        description="Public Key", 
        required=True,
        example="-----BEGIN PUBLIC KEY...END PUBLIC KEY-----\r\n"),
})

did_document_input_model = api.model('DIDDocument', {
    '@context': fields.String(
        description="Context attributes", 
        required=True,
        example='https://w3id.org/did/v1'),
    'id': fields.String(
        description="Decentralized IDentifier", 
        required=True,
        example="did:example:21tDAKCERh95uGgKbJNHY"),
    'authentication': fields.List(fields.Nested(auth_diddoc_model), 
        description="List of Authentication Mechanisms", 
        required=True),
    'service': fields.List(fields.Nested(service_output_model), 
        description="List of Service Endpoints", 
        required=True)
})

eidas_verify_credential_model = api.model('EIDASVerifyCredential', {
    'credential': fields.Nested(
        credential_input_model,
        description="Verifiable Credential to verify", 
        required=True),
    'did_document': fields.Nested(
        did_document_input_model, 
        description="DID Document", 
        required=True)
})

@eidas.route('/verify-credential')
class EIDASVerifyCredential(Resource):
    @eidas.expect(eidas_verify_credential_model)
    def post(self):
        """
        Verifies that the credential issuer had a valid eIDAS certificate at the moment of issuing the passed credential.

        Return "VALID" or Throws EIDASProofException on signature not valid
        """
        
        return eidas_verify_credential(
            request.json['credential'], 
            request.json['did_document']
        )

def init_api_server(host='0.0.0.0', port='5002'):
    # run api demo
    app.run(host, port)
    
if __name__ == '__main__':
    server_thread = threading.Thread(target=start_hub_server, daemon=True)

    # launch localhost server
    server_thread.start()
    # check if server started
    if server_thread.is_alive():
        # run demo
        app.run(host='0.0.0.0', port='5002')
     