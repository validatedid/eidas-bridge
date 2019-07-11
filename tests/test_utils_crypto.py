#test_utils_crypto.py
""" Unit test for cryptographic functions from utils/crypto.py file for eIDAS Library """

import pytest
from cryptography import x509
from tests.data.common_data import x509certs
from utils.crypto import x509_load_certificate_from_data_bytes
from cryptography.hazmat.backends import default_backend

@pytest.mark.parametrize("x509cert", x509certs)
def test_x509_load_certificate_from_data_bytes(x509cert):
    internal_cert = x509_load_certificate_from_data_bytes(x509cert)
    expected_cert = x509.load_pem_x509_certificate(x509cert, default_backend())
    assert internal_cert == expected_cert