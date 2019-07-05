
""" EIDAS BRIDGE """

def eidas_link_did(did, certificate, proof: str) -> str:
    """ 
    Link the Issuer DID with eIDAS certificate

    Receives a DID, an eIDAS certificate, and its proof of possession
    Returns the JSON that needs to be stored on the Agent public Storage
    (i.e: an Identity Hub)
    """
    return ""

def eidas_get_service_endpoint_struct(storage_endpoint: str) -> str:
    """ 
    Contructs the JSON structure that needs to be added to the Issuer's DID Document
    Receives a service endpoint where it is stored the issuer's 
    eIDAS and DID linking information and returns the correspondent JSON
    """
    return ""

def eidas_sign_credential(json_credential: str) -> str:
    """ 
    Checks the validity of the issuer's eIDAS certificate against a 
    Trusted Service Provider and adds the corresponde response to the 
    received credential JSON structure.
    """
    return ""

def eidas_verify_credential(json_credential: str) -> str:
    """
    Verifies that the credential issuer had a valid eIDAS certificate 
    at the moment of issuing the passed credential.
    Returns: VALID or NOT VALID
    """
    return "NOT VALID"