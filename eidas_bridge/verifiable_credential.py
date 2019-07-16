# verifiable_credential.py
""" Implementation of a Verifiable Credential defined in https://w3c.github.io/vc-data-model/ """

from .utils.util import check_args
import json

class VerifiableCredential():
    """ Represents a Verifiable Credential instance according to W3C spec """

    def __init__(self, json_credential):
        check_args(json_credential, str)
        self._verifiable_credential = json.loads(json_credential)
    
    def get_issuer_did(self) -> str:
        """ Returns the Issuer's DID from the Verifiable Credential """

        return self._verifiable_credential['credentialSubject']['id']
    
    def to_json(self) -> str:
        """
        Create a JSON representation of the model instance.

        Returns:
            A JSON representation of this message

        """

        return json.dumps(self._verifiable_credential, indent=4)


