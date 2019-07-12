#test_eidas_bridge_utils_crypto.py
""" Unit test for cryptographic functions from eidas_bridge/utils/crypto.py file for eIDAS Library """

import pytest
from cryptography import x509
from tests.data.common_data import eidas_link_inputs
from eidas_bridge.utils.crypto import x509_load_certificate_from_data_bytes
from cryptography.hazmat.backends import default_backend

@pytest.mark.parametrize("eidas_link_input", eidas_link_inputs)
def test_x509_load_certificate_from_data_bytes(eidas_link_input):
    internal_cert = x509_load_certificate_from_data_bytes(eidas_link_input[0])
    expected_cert = x509.load_pem_x509_certificate(eidas_link_input[0], default_backend())
    assert internal_cert == expected_cert