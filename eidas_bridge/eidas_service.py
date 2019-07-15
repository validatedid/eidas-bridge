# eidas_service.py
""" Represents an eIDAS Service Endpoint structure """

from .utils.util import check_args
import json

class EIDASService():
    """ Represents an eIDAS Service Endpoint structure """

    def __init__(self, did, endpoint):
        check_args(did, str)
        check_args(endpoint, str)

        self._did = did
        self._endpoint = endpoint

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
        "id": self._did + "#eidas",
        "type": "EidasService",
        "serviceEndpoint": self.endpoint
    }
