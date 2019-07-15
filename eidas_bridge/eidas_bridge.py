
# eidas_bridge.py
""" EIDAS BRIDGE """

from .utils.util import check_args
from .utils.crypto import PSS_PADDING
from .eidaslink import EIDASLink
from .eidas_service import EIDASService

class EIDASNotSupportedException(Exception):
    """
    Error raised when is called a library function than will not be supported 
    at this development Phase.
    """

def eidas_link_did(did, certificate, proof, padding = PSS_PADDING) -> str:
    """ 
    Link the Issuer DID with eIDAS certificate

    Receives a DID, an eIDAS certificate, its proof of possession, and 
    optionally the padding of the signature proof (accepts PKCS#1 and PSS)

    Returns the JSON that needs to be stored on the Agent public Storage
    (i.e: an Identity Hub)
    """
    
    return EIDASLink(did, certificate, proof, padding).to_json()

def eidas_get_service_endpoint(did, service_endpoint) -> str:
    """ 
    Contructs the JSON structure that needs to be added to the Issuer's 
    DID Document Service Endpoint Section. 

    Receives a did and a service endpoint where it is stored the issuer's 
    eIDAS and DID linking information.

    Returns the correspondent JSON to be added to the Service Endpoint 
    Section of the Issuer's DID Document.
    """

    return EIDASService(did, service_endpoint).to_json()

def eidas_sign_credential(json_credential) -> str:
    """ 
    Checks the validity of the issuer's eIDAS certificate against a 
    Trusted Service Provider and adds the corresponde response to the 
    received credential JSON structure.

    Not Supported at this Phase 0.
    """
    raise EIDASNotSupportedException("eIDAS library call NOT supported.")

def eidas_verify_credential(json_credential) -> str:
    """
    Verifies that the credential issuer had a valid eIDAS certificate 
    at the moment of issuing the passed credential.
    Returns: VALID or NOT VALID
    """
    check_args(json_credential, str)

     # TO DO 
    '''
    - Retrieve the DID from the credential
    - Resolve a DID Document from the DID
    - Get the storage endpoint to get the eIDAS json structure
    - Check that this DID has an eIDAS certificate (with a public key) 
        that can verify the proof stored
    - Retrieve the eIDAS json block structure from the credential
    - Check the validity of the certificate when the credential was issued
    - return the correspondent value
    '''

    return "NOT VALID"