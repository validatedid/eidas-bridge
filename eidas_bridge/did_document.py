# did_document.py
""" Implementation of a DID Document defined in https://w3c-ccg.github.io/did-spec/#did-documents """

from .utils.util import check_args
import json

class EIDASServiceEndpointException(Exception):
    """
    Error raised when no eIDAS Service Type is found in the DID Document.
    """

class DIDDocument():
    """ Represents a DID Document instance according to W3C spec """

    def __init__(self, json_did_document):

        self._did_document = json.loads(json_did_document)
    
    def get_did(self) -> str:
        """ Returns the DID Subject from the DID Document """

        return self._did_document['id']
    
    def get_eidas_service_endpoint(self) -> str:
        """ Returns the service endpoint to retrieve an EIDAS Link structure """

        eidas_service_endpoint = self._get_eidas_service_endpoint_from_did_doc()
        
        if eidas_service_endpoint == None:
            raise EIDASServiceEndpointException("No eIDAS Service Type is found in the DID Document.")
        
        return eidas_service_endpoint
    
    def _get_eidas_service_endpoint_from_did_doc(self) -> str:
        """ Returns the eidas service endoint inside a DID Document """

        # TO DO
        return "http://service_endpoint.sample/did:example:21tDAKCERh95uGgKbJNHYp/eidas"

