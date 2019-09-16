# crypto.py
""" Cryptographic auxiliary functions necessary to 
run tests but not necessary for the eidas library
"""

import datetime
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKeyWithSerialization
from cryptography.hazmat.primitives import serialization
from .util import print_object
from eidas_bridge.utils.crypto import PKCS1v15_PADDING, PSS_PADDING, InvalidPaddingException


class RSAKeySizeException(Exception):
    """Error raised when key length is not 2048 or 4096."""

""""""""""""""""""""""""
""" HASH FUNCTIONS """
""""""""""""""""""""""""
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

def _generate_x509_certificate(private_key, 
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
        private_key.public_key()
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
    ).sign(private_key, hashes.SHA256(), default_backend())

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

def store_key_and_x509cert_to_disk(privkey, key_pem_file, input_password,
    x509cert, x509cert_pem_file):
    _store_key_to_disk(privkey, key_pem_file, input_password)
    _x509_store_certificate_to_disk(x509cert, x509cert_pem_file)

def _store_key_to_disk(privkey, pem_key_file, input_password):
    # Write our key to disk for safe keeping
    with open(pem_key_file, "wb") as f:
        f.write(privkey.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(input_password),
        ))

def get_private_key_from_key_str(privkey, input_password) -> str:
    """ returns a string containing a private key in PEM format """
    return privkey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(input_password)
    )

def load_private_key_from_file(path_to_key_file, input_password) -> bytes:
    """ loads a private key from the specified file """
    with open(path_to_key_file, "rb") as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=input_password,
            backend=default_backend()
        )

def _load_private_key_from_data(pem_data, input_password) -> bytes:
    """ loads a private key object from a PEM data bytes """
    return serialization.load_pem_private_key(
        data=pem_data,
        password=input_password,
        backend=default_backend()
    )

def get_public_key_from_key_str(privkey) -> str:
    """ returns a string containing a public key in PEM format """
    public_key = privkey.public_key()
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def _load_public_key_from_data(pem_data) -> bytes:
    """ loads a public key object from a PEM public key data bytes """
    return serialization.load_pem_public_key(
        data=pem_data,
        backend=default_backend
    )

def _x509_store_certificate_to_disk(x509cert, pem_cert_file):
    # Write our certificate out to disk.
    with open(pem_cert_file, "wb") as f:
        f.write(x509cert.public_bytes(serialization.Encoding.PEM))

def x509_load_certificate_from_file(path_to_cert_file) -> bytes:
    """ loads a x509 certificate object from a PEM x509 certificate file """
    with open(path_to_cert_file, "rb") as key_file:
        return x509.load_pem_x509_certificate(key_file.read(), default_backend())

def x509_load_certificate_from_data_str(pem_data) -> bytes:
    """ loads a x509 certificate object from a PEM x509 certificate data in string format"""
    return x509.load_pem_x509_certificate(str(pem_data).encode("utf-8"), default_backend())

def x509_get_PEM_certificate_from_obj(x509cert) -> bytes:
    """ returns a PEM string with a x509 certificate """
    return x509cert.public_bytes(serialization.Encoding.PEM)

""" Nice stdout printing RSA key and x509 certificate """
def print_rsa_priv_key(rsa_key, input_password):
    priv_key = rsa_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(input_password)
        )
    print_object(priv_key)

def print_rsa_pub_key(rsa_pub_key):
    print_object(
        rsa_pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

def print_x509cert(x509cert):
    pem_cert = x509_get_PEM_certificate_from_obj(x509cert)
    print_object(pem_cert)

""""""""""""""""""""""""""""""""
""" SIGN & VERIFY FUNCTIONS """
""""""""""""""""""""""""""""""""

def rsa_sign(message, rsa_priv_key, padding_type):
    if padding_type == PSS_PADDING :
        return rsa_sign_pss(message, rsa_priv_key)
    elif padding_type == PKCS1v15_PADDING :
        return rsa_sign_pkcs1(message, rsa_priv_key)
    else: 
        raise InvalidPaddingException("Invalid Padding format: only supported PKCS#1 and PSS")

def rsa_sign_pss(message, rsa_priv_key) -> bytes:
    return rsa_priv_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

def rsa_sign_pkcs1(message, rsa_priv_key) -> bytes:
    return rsa_priv_key.sign(
        message,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

def ecdsa_sign(data, private_key) -> bytes:
    signature = private_key.sign(
        data,
        ec.ECDSA(hashes.SHA256())
    )
    return signature

def ecdsa_verify_priv(private_key, signature, data):
    public_key = private_key.public_key()
    public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))

def ecdsa_verify(public_key, signature, data):
    public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))

""""""""""""""""""""""""""""""
"""  ECDSA FUNCTIONS  """
""""""""""""""""""""""""""""""

def create_selfsigned_x509_certificate_ecdsa(cert_iss_country, cert_iss_state, 
cert_iss_locality, cert_iss_org, cert_iss_common, cert_valid_days) -> (bytes, bytes):
    """
        While most of the time you want a certificate that has been signed 
        by someone else (i.e. a certificate authority), so that trust is 
        established, sometimes you want to create a self-signed certificate. 
        Self-signed certificates are not issued by a certificate authority, 
        but instead they are signed by the private key corresponding 
        to the public key they embed.

        Returns:
        - an ECDSA key bytes object
        - a x509 certificate bytes object
    """
    private_key = _ecdsa_generate_key()
    x509Cert = _generate_x509_certificate(private_key, cert_iss_country, cert_iss_state, 
    cert_iss_locality, cert_iss_org, cert_iss_common, cert_valid_days)

    return private_key, x509Cert

def _ecdsa_generate_key() -> bytes:
    """ generate a ECDSA key with Secp256k1 as the default curve """
    return ec.generate_private_key(
        ec.SECP256K1(), default_backend()
    )

def _ecdsa_get_pubkey(private_key) -> bytes:
    """ returns the associated public key of a given ECDSA private key """
    return private_key.public_key()

def _ecdsa_serialize_pubkey(public_key) -> str:
    """" returns the serialized (string printable) format of a ECDSA public key """
    serialized_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return serialized_public.decode("utf-8")

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

""""""""""""""""""""""""""""""""
"""   PKCS#12 CERTIFICATE    """
""""""""""""""""""""""""""""""""

""" 
    CREATE .P12 FILE 
    command to create a .p12 file from the key and certificate created:
    $ openssl pkcs12 -export -out tests/data/certificate.p12 -inkey tests/data/rsakey.pem -in tests/data/x509cert.pem 
"""

def load_pkcs12_file(path_to_p12_file, input_password) ->(bytes, bytes, bytes):
    """ loads a key and certificate from a p12 file.
    Returns:	
        - A tuple of (private_key, certificate, additional_certificates)
    """
    with open(path_to_p12_file, "rb") as p12_file:
        p12_data = p12_file.read()
        return pkcs12.load_key_and_certificates(p12_data, input_password, default_backend())