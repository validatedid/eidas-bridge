# eidas_bridge_api.py
""" RESTFUL API for EIDAS BRIDGE """

import json, threading
from flask import Flask, request
from flask_restplus import Resource, Api, fields
from eidas_demo import init_server
from eidas_bridge.eidas_bridge import eidas_link_did, eidas_get_service_endpoint, \
    eidas_sign_credential, eidas_verify_credential, EIDASNotSupportedException
from eidas_bridge.utils.crypto import PSS_PADDING

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app, version='1.0', title='eIDAS Bridge API', description='An eIDAS bridge API to connect to a SSI solution')

eidas = api.namespace('eidas', description="eIDAS bridge API calls")

eidas_link_input_model = api.model('EIDASLink_in', {
    'did': fields.String(
        description="DID", 
        required=True,
        example="did:sov:55GkHamhTU1ZbTbV2ab9DE"),
    'certificate': fields.String(
        description="x509 certificate", 
        required=True,
        example="-----BEGIN CERTIFICATE-----\nMIIDYDCCAkigAwIBAgIUI63ffVceaNc1kN9O0q/4jSjbkU0wDQYJKoZIhvcNAQEL\nBQAwXTELMAkGA1UEBhMCRVMxEzARBgNVBAgMClRFU1RfU1RBVEUxEjAQBgNVBAcM\nCVRFU1RfQ0lUWTEQMA4GA1UECgwHQ0FfQUNNRTETMBEGA1UEAwwKbXlzaXRlLmNv\nbTAeFw0xOTA3MDkxNDA3MjBaFw0yMDA3MDgxNDA3MjBaMF0xCzAJBgNVBAYTAkVT\nMRMwEQYDVQQIDApURVNUX1NUQVRFMRIwEAYDVQQHDAlURVNUX0NJVFkxEDAOBgNV\nBAoMB0NBX0FDTUUxEzARBgNVBAMMCm15c2l0ZS5jb20wggEiMA0GCSqGSIb3DQEB\nAQUAA4IBDwAwggEKAoIBAQDm6RhyIeFZHn4bGQ/2UQ+aflczCo3Ej04LJXfiIU1Q\nt7xRq3e+uh7nTLffnS7fj/ZZBBREmR/D/SJBTlxv7WQEbscV/pf2LoZLjoC4M4ye\n43lUHRmWsm4J50tu9zcSheqXCRyAK/Ai6RUBy86NKXMFTUp/ONxS0BxJg8GU03Xd\nXGnYzdmZZXGDnublGYq03gD/cZYguS7/HS8v/MckdmjYPTy2syGL9unYkjWn7vig\niaDc2leAM4agKB6PODJSFla15HLoqskKX1SgtLJUHxu/FOo6hYdCt+GxpV1xhl/r\nEf3/SFeTZrJgL11m5ABDli2zAmCn4bjBNnNcXWy5QV0pAgMBAAGjGDAWMBQGA1Ud\nEQQNMAuCCWxvY2FsaG9zdDANBgkqhkiG9w0BAQsFAAOCAQEAYPUn0TzGyn438++1\nV2jMHC653C8tn3vVF5nTT7Td+ihc+KaaNDYsgyY2JpBIMRwlNgoNU0Da3P/9ZDn3\nlFJElUg8WpWPvpXtbS4udqn6UcfT9mFJtkzKg3CK5i50GRCabV9FPbY1bzYtUbY+\nEntXtI2h0dxcgzgOw6pkXFB3O7ZbbshpqWTlHtTtbxxrOFq0zcpyS92G+NTF6ASS\nhXcIf90du/mBWd2dinF/w2nkRAWfGBy8bGnUSJ93rPVwLjI0PDeHh7+PSQ+3X6mG\n5DI9EmzEC7esW6wJbhgiOYXLavAOmLfI0yq/z8SZMvFYwBE69VuGfPSj/u4nIhA5\nK0Qgnw==\n-----END CERTIFICATE-----\n"),
    'proof': fields.String(
        description="DID-hashed signature with public key", 
        required=True,
        example="4f1bb7069e1508901e83d9dd71043e35fbc8ecf3077625206dd00cf8f12365096cc1cf07822479e571689bc67c50a7d9ca66c43865e490044729af3356e853073073c11e9fa517f7b35748146c1c1101406f66866969ad5915054e3633ab3c247d6b09be909ece6d018ad309b1b34c45b223227d74928278640e0e6a62de0309309e609e8927eb7abd098dfb8a30e8c91fde3ea4fbe804b2967db2c994d303de1e6ac837cfd2a11414ace2bd75148e917b3505f17fabc4805484164a69fdc1d28122e977c1fa4f62b39a601915d8fe0b1bd6e2932db6c8ca3b2bca3ab04f3aebf83d081122d42248dc2a2f292f2c2bfc42244c3118109ab9f001a85cbdd52f71"),
    'padding': fields.String(
        description="Signature padding: PKCS1-v1_5 or PSS. Default = PSS", 
        default=PSS_PADDING,
        example="PSS",
        enum=['PSS', 'PKCS1-v1_5'])
})

proof_model = api.model('EIDAS_proof', {
    'type' : fields.String(
        description="Signature type", 
        required=True,
        example="RsaSignature2018"),
    'padding': fields.String(
        description="Signature padding: PKCS1-v1_5 or PSS", 
        required=True,
        example="PSS"),
    'signatureValue' : fields.String(
        description="DID-hashed signature with public key", 
        required=True,
        example="4f1bb7069e1508901e83d9dd71043e35fbc8ecf3077625206dd00cf8f12365096cc1cf07822479e571689bc67c50a7d9ca66c43865e490044729af3356e853073073c11e9fa517f7b35748146c1c1101406f66866969ad5915054e3633ab3c247d6b09be909ece6d018ad309b1b34c45b223227d74928278640e0e6a62de0309309e609e8927eb7abd098dfb8a30e8c91fde3ea4fbe804b2967db2c994d303de1e6ac837cfd2a11414ace2bd75148e917b3505f17fabc4805484164a69fdc1d28122e977c1fa4f62b39a601915d8fe0b1bd6e2932db6c8ca3b2bca3ab04f3aebf83d081122d42248dc2a2f292f2c2bfc42244c3118109ab9f001a85cbdd52f71")
})

eidas_link_output_model = api.model('EIDASLink_out', {
    'type': fields.String(
        description="Structure type: should be EidasLink", 
        required=True,
        example="EidasLink"),
    'created': fields.String(
        description="Structure datetime stamp creation: should be similar to '2002-10-10T17:00:00Z'", 
        required=True,
        example="2019-07-22 09:22:00.688300+00:00"),
    'did': fields.String(
        description="DID", 
        required=True,
        example="did:sov:55GkHamhTU1ZbTbV2ab9DE"),
    'certificate': fields.String(
        description="x509 certificate", 
        required=True,
        example="-----BEGIN CERTIFICATE-----\nMIIDYDCCAkigAwIBAgIUI63ffVceaNc1kN9O0q/4jSjbkU0wDQYJKoZIhvcNAQEL\nBQAwXTELMAkGA1UEBhMCRVMxEzARBgNVBAgMClRFU1RfU1RBVEUxEjAQBgNVBAcM\nCVRFU1RfQ0lUWTEQMA4GA1UECgwHQ0FfQUNNRTETMBEGA1UEAwwKbXlzaXRlLmNv\nbTAeFw0xOTA3MDkxNDA3MjBaFw0yMDA3MDgxNDA3MjBaMF0xCzAJBgNVBAYTAkVT\nMRMwEQYDVQQIDApURVNUX1NUQVRFMRIwEAYDVQQHDAlURVNUX0NJVFkxEDAOBgNV\nBAoMB0NBX0FDTUUxEzARBgNVBAMMCm15c2l0ZS5jb20wggEiMA0GCSqGSIb3DQEB\nAQUAA4IBDwAwggEKAoIBAQDm6RhyIeFZHn4bGQ/2UQ+aflczCo3Ej04LJXfiIU1Q\nt7xRq3e+uh7nTLffnS7fj/ZZBBREmR/D/SJBTlxv7WQEbscV/pf2LoZLjoC4M4ye\n43lUHRmWsm4J50tu9zcSheqXCRyAK/Ai6RUBy86NKXMFTUp/ONxS0BxJg8GU03Xd\nXGnYzdmZZXGDnublGYq03gD/cZYguS7/HS8v/MckdmjYPTy2syGL9unYkjWn7vig\niaDc2leAM4agKB6PODJSFla15HLoqskKX1SgtLJUHxu/FOo6hYdCt+GxpV1xhl/r\nEf3/SFeTZrJgL11m5ABDli2zAmCn4bjBNnNcXWy5QV0pAgMBAAGjGDAWMBQGA1Ud\nEQQNMAuCCWxvY2FsaG9zdDANBgkqhkiG9w0BAQsFAAOCAQEAYPUn0TzGyn438++1\nV2jMHC653C8tn3vVF5nTT7Td+ihc+KaaNDYsgyY2JpBIMRwlNgoNU0Da3P/9ZDn3\nlFJElUg8WpWPvpXtbS4udqn6UcfT9mFJtkzKg3CK5i50GRCabV9FPbY1bzYtUbY+\nEntXtI2h0dxcgzgOw6pkXFB3O7ZbbshpqWTlHtTtbxxrOFq0zcpyS92G+NTF6ASS\nhXcIf90du/mBWd2dinF/w2nkRAWfGBy8bGnUSJ93rPVwLjI0PDeHh7+PSQ+3X6mG\n5DI9EmzEC7esW6wJbhgiOYXLavAOmLfI0yq/z8SZMvFYwBE69VuGfPSj/u4nIhA5\nK0Qgnw==\n-----END CERTIFICATE-----\n"),
    'proof': fields.Nested(
        proof_model, 
        description="Signature proof structure", 
        required=True)
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

        return json.loads(
            eidas_link_did(
                request.json['did'], 
                request.json['certificate'], 
                request.json['proof'], 
                request.json['padding']
            )
        )

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

@eidas.route('/sign-credential')
class EIDASSignCredential(Resource):
    @eidas.expect(credential_input_model)
    def post(self):
        """ 
        Checks the validity of the issuer's eIDAS certificate against a Trusted Service Provider and adds the corresponde response to the received credential JSON structure.

        Not Supported at this Phase 0.
        """
        try:
            return eidas_sign_credential(request.get_json())
        except EIDASNotSupportedException:
            return "--- EIDAS Library function NOT supported yet. ---"

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

if __name__ == '__main__':
    server_thread = threading.Thread(target=init_server, daemon=True)

    # launch localhost server
    server_thread.start()
    # check if server started
    if server_thread.is_alive():
        # run demo
        app.run(port='5002')
     