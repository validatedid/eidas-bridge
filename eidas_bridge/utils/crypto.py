"""Cryptography and X509 certificate functions used by eIDAS Bridge."""

from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
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

""""""""""""""""""""""""
""" HASH FUNCTIONS """
""""""""""""""""""""""""
def eidas_crypto_hash_byte(b_data: bytes) -> bytes:
    """ Generates a 256-hash from bytes (using cryptography module) """
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(b_data)
    return digest.finalize()

""""""""""""""""""""""""""""""
"""  X509 FUNCTIONS  """
""""""""""""""""""""""""""""""

def x509_load_certificate_from_data_bytes(pem_data) -> bytes:
    """ loads a x509 certificate object from a PEM x509 certificate data already encoded """
    return x509.load_pem_x509_certificate(pem_data, default_backend())

def x509_get_PEM_certificate_from_obj(x509cert) -> bytes:
    """ returns a PEM string with a x509 certificate """
    return x509cert.public_bytes(serialization.Encoding.PEM)

def get_public_key_from_x509cert_obj(x509cert) -> bytes:
    """ returns a RSA public key object from a x509 certificate object """
    return x509cert.public_key()

def get_public_key_from_x509cert_pem(x509_pem) -> bytes:
    """ returns a RSA public key object from a x509 certificate in PEM format """
    x509cert = x509_load_certificate_from_data_bytes(x509_pem)
    return get_public_key_from_x509cert_obj(x509cert)

def x509_load_certificate_from_data_str(pem_data) -> bytes:
    """ loads a x509 certificate object from a PEM x509 certificate data in string format"""
    return x509.load_pem_x509_certificate(str(pem_data).encode("utf-8"), default_backend())

def get_public_key_from_x509cert_json(x509_str:str) -> dict:
    x509_obj = x509_load_certificate_from_data_str(x509_str)
    pubkey_obj = get_public_key_from_x509cert_obj(x509_obj)
    return { "publicKeyPem" : _ecdsa_serialize_pubkey(pubkey_obj) }


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

""""""""""""""""""""""""""""""
"""  ECDSA FUNCTIONS  """
""""""""""""""""""""""""""""""

def _ecdsa_serialize_privkey(private_key, input_password) -> str:
    """" returns the serialized (string printable) format of a ECDSA private key """
    if input_password is None:
        serialized_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    else:
        serialized_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(input_password)
        )
    return serialized_private.decode("utf-8")

def _ecdsa_serialize_pubkey(public_key) -> str:
    """" returns the serialized (string printable) format of a ECDSA public key """
    serialized_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return serialized_public.decode("utf-8")

def _load_private_key_from_data(pem_data, input_password) -> bytes:
    """ loads a private key object from a PEM data bytes """
    return serialization.load_pem_private_key(
        data=pem_data,
        password=input_password,
        backend=default_backend()
    )

def load_private_key_from_pem_str(pem_data_str:str, input_password) -> bytes:
    return _load_private_key_from_data(str(pem_data_str).encode("utf-8"), input_password)

def eidas_sign(privkey_str:str, input_password:bytes, message:bytes) -> bytes:
    priv_key = load_private_key_from_pem_str(privkey_str, input_password)
    return ecdsa_sign(message, priv_key)

def ecdsa_sign(data, private_key) -> bytes:
    signature = private_key.sign(
        data,
        ec.ECDSA(hashes.SHA256())
    )
    return signature

""""""""""""""""""""""""""""""""
"""   PKCS#12 CERTIFICATE    """
""""""""""""""""""""""""""""""""

def load_pkcs12_data(p12_data, input_password) ->(bytes, bytes, bytes):
    """ loads a key and certificate from a p12 data.
    Returns:	
        - A tuple of (private_key, certificate, additional_certificates)
    """
    return pkcs12.load_key_and_certificates(p12_data, input_password, default_backend())

def eidas_load_pkcs12(p12_data, input_password) -> (str, str):
    """ loads a key and certificate from a p12 data.
    Returns: 
        - A tuple of private_key, certificate in a serialized format
    """
    priv_key, x509cert, *_ = load_pkcs12_data(p12_data, input_password)

    serialized_key = _ecdsa_serialize_privkey(priv_key, input_password)
    serialized_cert = x509_get_PEM_certificate_from_obj(x509cert).decode()

    return serialized_key, serialized_cert