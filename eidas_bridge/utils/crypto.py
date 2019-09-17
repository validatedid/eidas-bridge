"""Cryptography and X509 certificate functions used by eIDAS Bridge."""

from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import pkcs12
from .util import check_args

""" PADDING CONSTANTS """
PKCS1v15_PADDING = "PKCS1-v1_5"
PSS_PADDING = "PSS"

class InvalidSignatureException(Exception):
    """Error raised when the signature is not valid """

class InvalidPaddingException(Exception):
    """ Error raised when the signature padding is neither PKCS#1 nor PSS """

def check_args_padding(padding, type_obj):
    check_args(padding, type_obj)
    if padding != PKCS1v15_PADDING and padding != PSS_PADDING:
        raise InvalidPaddingException("Invalid Padding format: only supported PKCS#1 and PSS")

""""""""""""""""""""""""""""""
"""  RSA & X509 FUNCTIONS  """
""""""""""""""""""""""""""""""

def x509_load_certificate_from_data_bytes(pem_data) -> bytes:
    """ loads a x509 certificate object from a PEM x509 certificate data already encoded """
    return x509.load_pem_x509_certificate(pem_data, default_backend())

def get_public_key_from_x509cert_obj(x509cert) -> bytes:
    """ returns a RSA public key object from a x509 certificate object """
    return x509cert.public_key()

def get_public_key_from_x509cert_pem(x509_pem) -> bytes:
    """ returns a RSA public key object from a x509 certificate in PEM format """
    x509cert = x509_load_certificate_from_data_bytes(x509_pem)
    return get_public_key_from_x509cert_obj(x509cert)

""""""""""""""""""""""""""""""""
"""   RSA VERIFY FUNCTIONS   """
""""""""""""""""""""""""""""""""

def rsa_verify(signature, message, rsa_pub_key, padding_type):
    if padding_type == PSS_PADDING :
        rsa_verify_pss(signature, message, rsa_pub_key)
    elif padding_type == PKCS1v15_PADDING :
        rsa_verify_pkcs1(signature, message, rsa_pub_key)
    else:
        raise InvalidPaddingException("Invalid Padding format: only supported PKCS#1 and PSS")

def rsa_verify_pss(signature, message, rsa_pub_key):
    try:
        rsa_pub_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    except InvalidSignature:
        raise InvalidSignatureException(InvalidSignature)

def rsa_verify_pkcs1(signature, message, rsa_pub_key):
    try:
        rsa_pub_key.verify(
            signature,
            message,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
    except InvalidSignature:
        raise InvalidSignatureException(InvalidSignature)

""""""""""""""""""""""""""""""""
"""   PKCS#12 CERTIFICATE    """
""""""""""""""""""""""""""""""""

def load_pkcs12_data(p12_data, input_password) ->(bytes, bytes, bytes):
    """ loads a key and certificate from a p12 data.
    Returns:	
        - A tuple of (private_key, certificate, additional_certificates)
    """
    return pkcs12.load_key_and_certificates(p12_data, input_password, default_backend())