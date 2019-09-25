# verifiable_credential.py
""" Implementation of a Verifiable Credential defined in https://w3c.github.io/vc-data-model/ """

from .utils.util import check_args
from eidas_bridge.utils.lds_ecdsa_secp256k1_2019 import sign
from eidas_bridge.utils.crypto import load_private_key_from_pem_str
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
    
    def get_proof_kid(self) -> str:
        """ Returns the Key Identifier from the Proof Section """
        # !!! TBD
        return ""
        
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
        # decipher private key and convert it to an object
        private_key = load_private_key_from_pem_str(privkey, input_password)
        # generate a LD-Proof from a LD Signature
        proof = sign(self._verifiable_credential, self.get_issuer_did()+'#eidas-keys-1', private_key)
        # add proof to the existing credential
        self._add_element('proof', proof)
        """
        # add new context value to accept lds-ecdsa-secp256k1-2019 jws signatures
        context = {
            "@context" : "https://w3id.org/security/v2"
        }
        self._add_element('@context', context)
        """
    
    def _add_element(self, key, value):
        # checking if key exists in credential and key is not empty {}
        if key in self._verifiable_credential and self._verifiable_credential[key]:
            # check if it is a dict instance and create a list to insert new element
            if isinstance(self._verifiable_credential[key], dict):
                tmp_value = self._verifiable_credential[key]
                # create new empty list
                self._verifiable_credential[key] = []
                # add the existant value
                self._verifiable_credential[key].append(tmp_value)
            # add proof to the existing credential proof list
            self._verifiable_credential[key].append(value)
        else:
            self._verifiable_credential.update( { key : value } )
    
    def verify(self, public_key:str) -> str:
        """
        Verifies the credential proof signature using the given public key.
        Returns "VALID" or throws EIDASProofException on signarure not valid
        """
        # !!! TBD
        return "VALID"



 


