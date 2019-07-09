# test_crypto.py

import pytest
from utils.crypto import eidas_crypto_hash_str, x509_load_certificate_from_data_bytes
from tests.data.common_data import crypto_testdata, x509certs
from cryptography import x509
from cryptography.hazmat.backends import default_backend

@pytest.mark.parametrize("did, expected", crypto_testdata)
def test_eidas_crypto_hash_str(did, expected):
    assert eidas_crypto_hash_str(did) == expected

@pytest.mark.parametrize("x509cert", x509certs)
def test_x509_load_certificate_from_data_bytes(x509cert):
    internal_cert = x509_load_certificate_from_data_bytes(x509cert)
    expected_cert = x509.load_pem_x509_certificate(x509cert, default_backend())
    assert internal_cert == expected_cert

""" code to load a certificate from file """
"""
    with open("./tests/data/tmp/x509cert.pem", "rb") as cert_file:
        data = cert_file.read()

"""