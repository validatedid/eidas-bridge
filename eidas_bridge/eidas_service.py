# eidas_service.py
""" Represents an eIDAS Service Endpoint structure """

from .utils.util import check_args, clean_did
import json

class EIDASGetEidasLinkException(Exception):
     """Error raised when the server endpoint returned an error on an eidas link request """

class EIDASService():
    """ Represents an eIDAS Service Endpoint structure """

    EIDAS_SERVICE_TYPE = "EidasService"
    EIDAS_SERVICE_FRAGMENT = "#eidas"

    def __init__(self, did, endpoint):
        check_args(did, str)
        check_args(endpoint, str)

        # remove all possible delimiters '#', ';', '?'
        self._did = clean_did(did)
        self._endpoint = endpoint
    
    @classmethod
    def from_json(cls, eidas_service_as_json: str) -> 'EIDASService':
        eidas_str = json.loads(eidas_service_as_json)
        return cls(
            did=clean_did(eidas_str['did']), 
            endpoint=eidas_str['serviceEndpoint']
        )

    def get_endpoint(self) -> str:
        return self._endpoint

    def to_json(self) -> str:
            """
            Create a JSON representation of the model instance.

            Returns:
                A JSON representation of this message

            """
            return json.dumps(self._serialize(), indent=1)

    def _serialize(self) -> str:
        """
        Dump current object to a JSON-compatible dictionary.

        Returns: 
            dict representation of current eIDAS Service Endpoint
        """
        return {
            "id": self._did + EIDASService.EIDAS_SERVICE_FRAGMENT,
            "type": EIDASService.EIDAS_SERVICE_TYPE,
            "serviceEndpoint": self._endpoint
            }
