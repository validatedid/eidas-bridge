
# eidas_bridge.py
""" EIDAS BRIDGE """

from .eidas_service import EIDASService
from .verifiable_credential import VerifiableCredential
from .did_document import DIDDocument
from .eidas_qec import EIDASQEC, EIDASOCSPCertificateException
from .utils.crypto import eidas_load_pkcs12, get_public_key_from_x509cert_json
from .utils.dbmanager import DBManager
import json

class EIDASPublicKeyException(Exception):
    """
    Error raised when Public key from DID Document differs from QEC's public key
    """

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

def eidas_get_pubkey(did:str) -> str:
    """
    From a given DID, returns the correspondent public key json struct.

    Returns: { "publicKeyPem" : "-----BEGIN PUBLIC KEY...END PUBLIC KEY-----\n" }

    Cryptographic keys currently supported format are only Secp256k1.
    """
    # instantiate the DB file to store the data
    dbmanager = DBManager()
    # get certificate stored in DB and retrieve public key's serialized format
    return json.dumps(get_public_key_from_x509cert_json(dbmanager.get_qec(did)), indent=1)

def eidas_sign_credential(credential) -> str:
    """ 
    Adds a digital signature to the given credential, generated with an eIDAS private key.

    Returns the correspondent Verifiable Credential.

    Cryptographic keys currently supported format are only Secp256k1.
    """

    # Constructs a Verifiable Credential object and gets the issuer's did
    verifiable_credential = VerifiableCredential(credential)
    issuer_did = verifiable_credential.get_issuer_did()
    #instantiate the DB file to store the data
    dbmanager = DBManager()
    # get private key and password to sign
    key, password = dbmanager.get_key(issuer_did)
    # assure password is in bytes format
    if isinstance(password, str):
        password = password.encode("utf-8")
    # signs and adds the signature to the credential
    verifiable_credential.sign_and_add_proof(key, password)
    # return in json string format
    return verifiable_credential.to_json()

def eidas_verify_credential(credential, json_did_document) -> str:
    """
    Verifies that the credential issuer had a valid eIDAS certificate at the moment of issuing the passed credential. Throws EIDASProofException on signarure not valid.

    The current implementation does NOT support for DID resolution.

    The algorithm executes the following procedure:

    1. Get DID from the credential and from did_document and check they are the same
    2. Get key identifier from proof section from the credential and retrieve the public key PEM format from the did document that matches the extracte key identifier
    3. Get EidasService service endpoint from did_document to be able to access the Issuer's Identity Hub
    4. Retrieve QEC from the Issuer's Identity Hub and extract its public key
    5. Validate OCSP Certificate: Throws EIDASOCSPCertificateException otherwise
    6. Check that the public key from the QEC is the same as the one stored in the did document: Throws EIDASPublicKeyException on mismatch.
    7. Validate credential proof signature: Throws EIDASProofException on signature not valid (NOT IMPLEMENTED)
    8. Return VALID
    """

    # Constructs a Verifiable Credential object and gets the issuer's did
    vc = VerifiableCredential(credential)
    did_from_cred = vc.get_issuer_did()
    proof_kid = vc.get_proof_kid()

    # Constructs a DID Document object ang gets the did subject
    did_document = DIDDocument(json_did_document)
    did_from_doc = did_document.get_did()

    if not did_from_cred == did_from_doc:
        raise EIDASDIDMismatchException("Issuer's DID differs from the DID_Document's DID subject")
    
    # Extracts the eIDAS service endpoint from Did Document
    eidas_service = did_document.get_eidas_service_endpoint()
    # get QEC stored in Identity Hub
    eidas_qec = EIDASQEC(eidas_service.get_endpoint())
    # Throws EIDASOCSPCertificateException on OCSP validation error
    if not eidas_qec.OCSP_valid():
        raise EIDASOCSPCertificateException("Error on OCSP certificate validation.")
    # Throws EIDASPublicKeyException in case public keys differs
    if not did_document.get_pubkey(proof_kid) == eidas_qec.get_pubkey():
        raise EIDASPublicKeyException("Public keys from eiDAS QEC and Did Document mismatch.")
    # Returns "VALID" or throws EIDASProofException on signarure not valid
    return vc.verify(eidas_qec.get_pubkey())