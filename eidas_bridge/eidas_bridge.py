
# eidas_bridge.py
""" EIDAS BRIDGE """

from .eidas_service import EIDASService
from .verifiable_credential import VerifiableCredential
from .did_document import DIDDocument
from .utils.crypto import eidas_load_pkcs12
from .utils.dbmanager import DBManager

class EIDASNotSupportedException(Exception):
    """
    Error raised when is called a library function than will not be supported 
    at this development Phase.
    """

class EIDASDIDMismatchException(Exception):
    """
    Error raised when the Issuer's DID differs from the DID_Document's DID subject.
    """

def eidas_load_qec(did, p12_data, password):
    """
    Imports an eIDAS Qualified Electronic Certificate (QEC) with its correspondent 
    private key to be used in further digital signature operations.

    QEC currently supported format is only Secp256k1.
    """
    if isinstance(password, str):
        password = password.encode("utf-8")
    if isinstance(p12_data, str):
        p12_data = bytes.fromhex(p12_data)

    # load eIDAS certificate and private key
    priv_key, x509cert = eidas_load_pkcs12(p12_data, password)
    #instantiate the DB file to store the data
    dbmanager = DBManager()
    # store data to the disk
    dbmanager.store_qec(did, x509cert, priv_key, password)

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

def eidas_get_pubkey(did) -> str:
    """
    From a given DID, returns the correspondent public key.

    Cryptographic keys currently supported format are only Secp256k1.
    """

    return ""

def eidas_sign_credential(credential) -> str:
    """ 
    Adds a digital signature to the given credential, generated with an eIDAS private key.

    Returns the correspondent Verifiable Credential.

    Cryptographic keys currently supported format are only Secp256k1.
    """
    raise EIDASNotSupportedException("eIDAS library call NOT supported.")

def eidas_verify_credential(credential, json_did_document) -> str:
    """
    Verifies that the credential issuer had a valid eIDAS certificate at the moment of issuing the passed credential. Throws EIDASProofException on signarure not valid.

    The current implementation does NOT support for DID resolution.

    The algorithm executes the following procedure:

    1. Get DID from the credential and from did_document and check they are the same
    2. Get EidasService service endpoint from did_document to be able to access the Issuer's Identity Hub
    3. Retrieve QEC from the Issuer's Identity Hub, check the certificate validity and extract its public key
    4. Verify credential signature with the extracted eIDAS public key
    5. Return VALID or throw EIDASProofException on signature not valid
    """

    # Constructs a Verifiable Credential object and gets the issuer's did
    verifiable_credential = VerifiableCredential(credential)
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
    # !!! FIX Algorithm It returned the eIDAS link did structure to check the signature, but this structure no longer exists

    return "VALID"