# did_document.py
""" Implementation of a DID Document defined in https://w3c-ccg.github.io/did-spec/#did-documents """

import json

from typing import List

from .utils.util import check_args, get_did_in_service, get_fragment_in_service
from .service import Service
from .eidas_service import EIDASService

class EIDASPublicKeyException(Exception):
    """ Error raised when no eIDAS Public Key is found in the DID Document """

class EIDASServiceEndpointException(Exception):
    """
    Error raised when no eIDAS Service Type is found in the DID Document.
    """
class EIDASDIDDocNoSubjectIdException(Exception):
    """Error raised when a DID Document does not contain a Subject DID (id property)."""

class EIDASDIDDocNoServiceException(Exception):
     """Error raised when a DID Document does not contain a service property."""

class DIDDocument():
    """ Represents a DID Document instance according to W3C spec """

    def __init__(self, json_did_document):
        check_args(json_did_document, dict)
        self._did_document = json_did_document
        # checks for id property and returns it or throws an exception
        self._did = self._check_id_property_exist()
        # checks for service property
        self._check_service_property_exist()
        # sets all services checking if eidas_service exists, throwing an exception otherwise
        self._service, self._eidas_service = _get_services(self._did_document['service'])
    
    def get_did(self) -> str:
        """ Returns the DID Subject from the DID Document """
        return self._did
    
    def get_eidas_service_endpoint(self) -> EIDASService:
        """ Returns an EIDAS Service to retrieve an EIDAS Link structure """
        return self._eidas_service
    
    def get_eidas_pubkey(self, kid:str) -> str:
        """ Returns a public key in PEM string format identified by kid """
        # sets all services checking if eidas_service exists, throwing an exception otherwise
        return _get_key(self._did_document['authentication'], kid)

    def _check_id_property_exist(self) -> str:
        """ checks for the id property and throws an exception otherwise """
        try:
            return self._did_document['id']
        except KeyError:
            raise EIDASDIDDocNoSubjectIdException("A DID Document MUST have an id property.")
    
    def _check_service_property_exist(self):
        """ checks for the service property and throws an exception otherwise """
        try:
            self._did_document['service']
        except KeyError:
            raise EIDASDIDDocNoServiceException("A DID Document MUST have a service property.")

    def to_json(self) -> str:
        """
        Create a JSON representation of the model instance.

        Returns:
            A JSON representation of this message

        """
        return json.dumps(self._did_document, indent=4)

""""""""""""""""""
""" AUX METHODS """
""""""""""""""""""
def _get_services(services: list) -> (List[Service], EIDASService):
    """ Get a List of Service objects from the service property of a DID Document """
    list_services = []
    eidas_service = None

    for a_service in services:
        svc = Service (
            did = get_did_in_service(a_service['id']),
            ident = get_fragment_in_service(a_service['id']),
            typ = a_service['type'],
            endpoint = a_service['serviceEndpoint']
        )
        list_services.append(svc)
        # sets an eidas service in case the type matches
        eidas_service = _set_eidas_service(a_service)
    
    if eidas_service == None:
        raise EIDASServiceEndpointException("No eIDAS Service Type is found in the DID Document.")
   
    return list_services, eidas_service

def _get_key(keys: list, kid: str) -> str:
    """ Get a public key PEM string from the publicKey property of a DID Document """
    eidas_pub_key = None
    
    for a_key in keys:
        if a_key['id'] == kid:
            eidas_pub_key = a_key['publicKeyPem']
    
    if eidas_pub_key == None:
        raise EIDASPublicKeyException("No eIDAS Public Key is found in the DID Document.")
   
    return eidas_pub_key

def _set_eidas_service(a_service: dict) -> EIDASService:
    """ checks if the given service endpoint is an EIDAS type and returns the correspondent object """
    eidas_service = None

    if a_service['type'] == EIDASService.EIDAS_SERVICE_TYPE:
        eidas_service = EIDASService (
            did = get_did_in_service(a_service['id']),
            endpoint = a_service['serviceEndpoint']
        )
    
    return eidas_service
    

