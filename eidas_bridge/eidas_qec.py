# eidas_qec.py
""" Represents an eIDAS Qualified Electronic Certificate """

import requests

class EIDASOCSPCertificateException(Exception):
    """ Error raised when the OCSP validation returned error or not QEC stored """

class EIDASGetQECException(Exception):
     """Error raised when the server endpoint returned an error on an eidas qec request """

class EIDASQEC():
    """ Represents an eIDAS Qualified Electronic Certificate """
    def __init__(self, endpoint_uri:str):
        self._qec = _get_eidas_qec(endpoint_uri)
    
    def OCSP_valid(self) -> bool:
        """ Performs an OCSP validation """
        if not self._qec:
            raise EIDASOCSPCertificateException("QEC object not stored.")
        # currently NOT supported
        return True
    
    def get_pubkey(self) -> str:
        """ Returns certificate's public key in PEM string """
        # !!! TBD
        return ""



def _get_eidas_qec(uri:str) -> str:
    """ Retrieves a Qualified Electronic Certificate object using the eIDAS Service Endpoint """
    # retrieves the json eidas structure
    r = requests.get(uri)

    if not r.status_code == 200:
        raise EIDASGetQECException("Service Endpoint Error: EIDAS QEC data cannot be retrieved.")
    
    return r.json()