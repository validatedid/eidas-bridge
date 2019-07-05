
# eidas_bridge.py
""" EIDAS BRIDGE """

import util 

def eidas_link_did(did, certificate, proof) -> str:
    """ 
    Link the Issuer DID with eIDAS certificate

    Receives a DID, an eIDAS certificate, and its proof of possession
    Returns the JSON that needs to be stored on the Agent public Storage
    (i.e: an Identity Hub)
    """
    util.check_args(did, str)
    util.check_args(certificate, bytes)
    util.check_args(proof, bytes)

    # TO DO 
    '''
    - construct a json structure with the given parameters and return it
    - check that the proof really correspond to a PKCS#1 signature of
        the DID passed signed with the privkey of the certificate
    '''
    

    return ""

def eidas_get_service_endpoint_struct(storage_endpoint) -> str:
    """ 
    Contructs the JSON structure that needs to be added to the Issuer's DID Document
    Receives a service endpoint where it is stored the issuer's 
    eIDAS and DID linking information and returns the correspondent JSON
    """
    util.check_args(storage_endpoint, str)

     # TO DO 
    '''
    - construct a json structure with the given parameters and return it

    '''

    return ""

def eidas_sign_credential(json_credential) -> str:
    """ 
    Checks the validity of the issuer's eIDAS certificate against a 
    Trusted Service Provider and adds the corresponde response to the 
    received credential JSON structure.
    """
    util.check_args(json_credential, str)

     # TO DO 
    '''
    - construct a json structure with the given parameters and return it
    - launch an OCSP request to check the validity of the certificate
    '''

    return ""

def eidas_verify_credential(json_credential) -> str:
    """
    Verifies that the credential issuer had a valid eIDAS certificate 
    at the moment of issuing the passed credential.
    Returns: VALID or NOT VALID
    """
    util.check_args(json_credential, str)

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