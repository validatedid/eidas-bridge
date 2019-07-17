
# eidas_bridge.py
""" EIDAS BRIDGE """

from .utils.util import check_args
from .utils.crypto import PSS_PADDING
from .eidaslink import EIDASLink, EIDASProofException
from .eidas_service import EIDASService
from .verifiable_credential import VerifiableCredential
from .did_document import DIDDocument

class EIDASNotSupportedException(Exception):
    """
    Error raised when is called a library function than will not be supported 
    at this development Phase.
    """

class EIDASDIDMismatchException(Exception):
    """
    Error raised when the Issuer's DID differs from the DID_Document's DID subject.
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

def eidas_verify_credential(json_credential, json_did_document) -> str:
    """
    Verifies that the credential issuer had a valid eIDAS certificate 
    at the moment of issuing the passed credential.

    Throws EIDASProofException on signarure not valid
    """
    """ 
        ALGORITHM DESCRIPTION 

        eIDAS API function eidas_verify_credential should work on two ways:

        1. No support for DID resolution.
            In an initial and simpler phase, eIDAS library will delegate the DID resolution to the Agent, making the library simpler and completely independent of the DID-method used.
            In this scenario the API function will need the DID Document and the function will be as shown:

            def eidas_verify_credential(json_credential, did_document) -> str:

            The algorithm in this case would be as followed:

            * Get DID from the json_credential and from did_document and check are the same
            * Get EIDASLink service endpoint from did_document
            * Retrieve the EIDAS Link json structure and check that the DID correspond to the one from did_document
            * Verify signature with the public key of the EIDAS Link and the proof that contains
            * Throw EIDASProofException on signarure not valid

        2. Support for DID Resolution.
            In this case, the DID resolution would be responsibility for the eIDAS Library and it will not be necessary to include the DID Document as a parameter.

            def eidas_verify_credential(json_credential, did_document = None) -> str:

            The algorithm in this case will add one additional step:

            * Get DID from the json_credential
            * Resolve the DID and obtain the DID Document (using Universal Resolver component)
            * Get EIDASLink service endpoint from did_document
            * Retrieve the EIDAS Link json structure and check that the DID correspond to the one from did_document
            * Verify signature with the public key of the EIDAS Link and the proof that contains
            * Throw EIDASProofException on signarure not valid
    """

    # Constructs a Verifiable Credential object and gets the issuer's did
    verifiable_credential = VerifiableCredential(json_credential)
    did_from_cred = verifiable_credential.get_issuer_did()

    # Constructs a DID Document object ang gets the did subject
    did_document = DIDDocument(json_did_document)
    did_from_doc = did_document.get_did()

    if not did_from_cred == did_from_doc:
        raise EIDASDIDMismatchException("Issuer's DID differs from the DID_Document's DID subject")
    
    # Creates an EIDAS Service Endpoint to retrieve the EIDAS Link DID Structure 
    eidas_service = did_document.get_eidas_service_endpoint()
    # checks the signature in the EIDAS Link constructor
    # Throws EIDASProofException on signarure not valid
    EIDASLink.from_json(eidas_service.get_eidas_link_did())

    return "VALID"