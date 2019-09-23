# verifiable_credential.py
""" Implementation of a Verifiable Credential defined in https://w3c.github.io/vc-data-model/ """

from .utils.util import check_args
import json

class EIDASVerifiableCredentialNoIssuerException(Exception):
    """Error raised when a Verifiable Credential does not contain a Issuer DID."""

class VerifiableCredential():
    """ Represents a Verifiable Credential instance according to W3C spec """

    def __init__(self, json_credential):
        check_args(json_credential, dict)
        self._verifiable_credential = json_credential
        #checks for issuer property
        self._check_issuer_did_exist()
    
    def get_issuer_did(self) -> str:
        """ Returns the Issuer's DID from the Verifiable Credential """
        return self._verifiable_credential['issuer']
        
    def to_json(self) -> str:
        """
        Create a JSON representation of the model instance.

        Returns:
            A JSON representation of this message

        """
        return json.dumps(self._verifiable_credential, indent=4)
    
    def _check_issuer_did_exist(self):
        """ checks for the issuer property and throw an exception otherwise """
        try:
            self._verifiable_credential['issuer']
        except KeyError:
            raise EIDASVerifiableCredentialNoIssuerException("A Verifiable Credential MUST have an issuer property.")
    
    def sign_and_add_proof(self, privkey:str, input_password:bytes):
        """
        Generates a Linked Data Proof from a Linked Data Signature of the credential using a ES256K algorithm
        and adds the json-ld resultant to the credential structure

        Parameters:
            - privkey: an string representation of a PEM encoded ECDSA secp256k1 private key
            - password: an utf-8 encoded bytes from the password string to decipher private key

        """
 


