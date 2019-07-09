"""Cryptography and X509 certificate functions used by eIDAS Bridge."""

import datetime
import pysodium
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from .util import print_object


class RSAKeySizeException(Exception):
    """Error raised when key length is not 2048 or 4096."""

""""""""""""""""""""""""
""" HASHES FUNCTIONS """
""""""""""""""""""""""""
def eidas_hash_byte(b_data: bytes) -> str:
    """ Generates a 256-hash hex string from bytes """
    return pysodium.crypto_hash_sha256(b_data).hex()

def eidas_hash_str(str_data: str) -> str:
    """ Generates a 256-hash hex string from a given text string (using libsodium) """
    return eidas_hash_byte(str_data.encode('utf8'))

def eidas_hash_hex(hex_data: str) -> str:
    """ Generates a 256-hash hex string from a given hex string data """
    return eidas_hash_byte(bytes.fromhex(hex_data))

def eidas_crypto_hash_byte(b_data: bytes) -> str:
    """ Generates a 256-hash hex string from bytes (using cryptography module) """
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(b_data)
    return digest.finalize().hex()

def eidas_crypto_hash_str(str_data: str) -> str:
    """ Generates a 256-hash hex string from a given text string (using cryptography module) """
    return eidas_crypto_hash_byte(str_data.encode('utf8'))

def eidas_crypto_hash_hex(hex_data: str) -> str:
    """ Generates a 256-hash hex string from a given hex string data (using cryptography module) """
    return eidas_crypto_hash_byte(bytes.fromhex(hex_data))

""""""""""""""""""""""""""""""
"""  RSA & X509 FUNCTIONS  """
""""""""""""""""""""""""""""""
def _rsa_generate_key(key_size) -> bytes:
    """ Generate a RSA key """
    if key_size != 2048 and key_size != 4096:
        raise RSAKeySizeException("Only supported 2048 or 4096 RSA key lenght")
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )

def _rsa_store_key_to_disk(rsa_key, pem_key_file):
    # Write our key to disk for safe keeping
    with open(pem_key_file, "wb") as f:
        f.write(rsa_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase"),
        ))

def _generate_x509_certificate(rsa_key, 
    cert_iss_country, cert_iss_state, cert_iss_locality, cert_iss_org, cert_iss_common, 
    cert_valid_days) -> bytes:
    """ Create a x509 certificate signed with the given private key """
    # Various details about who we are. For a self-signed certificate the
    # subject and issuer are always the same.
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, cert_iss_country),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, cert_iss_state),
        x509.NameAttribute(NameOID.LOCALITY_NAME, cert_iss_locality),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, cert_iss_org),
        x509.NameAttribute(NameOID.COMMON_NAME, cert_iss_common),
    ])

    return x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        rsa_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        # Our certificate will be valid for cert_valid_days days
        datetime.datetime.utcnow() + datetime.timedelta(days=cert_valid_days)
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    # Sign our certificate with our private key
    ).sign(rsa_key, hashes.SHA256(), default_backend())

def _x509_store_certificate_to_disk(x509cert, pem_cert_file):
    # Write our certificate out to disk.
    with open(pem_cert_file, "wb") as f:
        f.write(x509cert.public_bytes(serialization.Encoding.PEM))

def create_selfsigned_x509_certificate(key_size,
    cert_iss_country, cert_iss_state, cert_iss_locality, cert_iss_org, cert_iss_common, 
    cert_valid_days) -> (bytes, bytes):
    """
        While most of the time you want a certificate that has been signed 
        by someone else (i.e. a certificate authority), so that trust is 
        established, sometimes you want to create a self-signed certificate. 
        Self-signed certificates are not issued by a certificate authority, 
        but instead they are signed by the private key corresponding 
        to the public key they embed.

        Returns:
        - a RSA key bytes object
        - a x509 certificate bytes object
    """
    rsa_key = _rsa_generate_key(key_size)
    x509Cert = _generate_x509_certificate(rsa_key, cert_iss_country, cert_iss_state, 
    cert_iss_locality, cert_iss_org, cert_iss_common, cert_valid_days)

    return rsa_key, x509Cert

def store_rsa_key_and_x509cert_to_disk(rsa_key, rsa_key_pem_file, x509cert, x509cert_pem_file):
    _rsa_store_key_to_disk(rsa_key, rsa_key_pem_file)
    _x509_store_certificate_to_disk(x509cert, x509cert_pem_file)

def get_public_key_from_rsakey_str(rsa_key) -> str:
    """ returns a string containing a RSA public key in PEM format """
    public_key = rsa_key.public_key()
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def get_public_key_from_x509cert_obj(x509cert) -> bytes:
    """ returns a RSA public key object from a x509 certificate object """
    return x509cert.public_key()

def get_private_key_from_rsakey_str(rsa_key, input_password) -> str:
    """ returns a string containing a RSA private key in PEM format """
    return rsa_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(input_password)
    )

def rsa_load_private_key_from_file(path_to_key_file, input_password) -> bytes:
    """ loads a RSA private key from the specified file """
    with open(path_to_key_file, "rb") as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=input_password,
            backend=default_backend()
        )

def rsa_load_public_key_from_data(pem_data) -> bytes:
    """ loads a RSA public key object from a PEM public key data string """
    return serialization.load_pem_public_key(
        data=pem_data,
        backend=default_backend
    )

def rsa_load_private_key_from_data(pem_data, input_password) -> bytes:
    """ loads a RSA private key object from a PEM public key data string """
    return serialization.load_pem_private_key(
        data=pem_data,
        password=input_password,
        backend=default_backend()
    )

def x509_load_certificate_from_data(pem_data) -> bytes:
    """ loads a x509 certificate object from a PEM x509 certificate data """
    return x509.load_pem_x509_certificate(pem_data, default_backend())

def x509_load_certificate_from_file(path_to_cert_file) -> bytes:
    """ loads a x509 certificate object from a PEM x509 certificate file """
    with open(path_to_cert_file, "rb") as key_file:
        return x509.load_pem_x509_certificate(key_file.read(), default_backend())

def x509_get_certificate_from_obj_str(x509cert) -> str:
    """ returns a PEM string with a x509 certificate """
    return x509cert.public_bytes(serialization.Encoding.PEM)

""" Nice stdout printing RSA key and x509 certificate """
def print_rsa_key(rsa_key):
    print_object(get_public_key_from_rsakey_str(rsa_key))

def print_x509cert(x509cert):
    print_object(x509_get_certificate_from_obj_str(x509cert))
    
