#test_eidas_bridge_utils_crypto.py
""" Unit test for cryptographic functions from eidas_bridge/utils/crypto.py file for eIDAS Library """

import pytest
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from tests.data.common_data import eidas_link_inputs, bad_obj_type_paddings, paddings, bad_type_paddings, \
    PKCS1v15_PADDING, PSS_PADDING
from eidas_bridge.utils.crypto import x509_load_certificate_from_data_bytes, check_args_padding, \
        InvalidPaddingException, get_public_key_from_x509cert_obj, get_public_key_from_x509cert_pem
from cryptography.hazmat.backends import default_backend

@pytest.mark.parametrize("padding", paddings)
def test_check_args_padding(padding):
    check_args_padding(padding, str)
    pass

@pytest.mark.parametrize("padding", bad_obj_type_paddings)
def test_check_args_padding_bad_obj_type(padding):
    with pytest.raises(TypeError):
        check_args_padding(padding, str)

@pytest.mark.parametrize("padding", bad_type_paddings)
def test_check_args_padding_bad_type(padding):
    with pytest.raises(InvalidPaddingException):
        check_args_padding(padding, str)

@pytest.mark.parametrize("eidas_link_input", eidas_link_inputs)
def test_x509_load_certificate_from_data_bytes(eidas_link_input):
    internal_cert = x509_load_certificate_from_data_bytes(eidas_link_input[0])
    expected_cert = x509.load_pem_x509_certificate(eidas_link_input[0], default_backend())
    assert internal_cert == expected_cert

@pytest.mark.parametrize("eidas_link_input", eidas_link_inputs)
def test_get_public_key_from_x509cert_obj(eidas_link_input):
        x509cert_obj = x509_load_certificate_from_data_bytes(eidas_link_input[0])
        pub_key_expected = x509cert_obj.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        returned_pub_key = get_public_key_from_x509cert_obj(x509cert_obj).public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        assert pub_key_expected == returned_pub_key

@pytest.mark.parametrize("eidas_link_input", eidas_link_inputs)
def test_get_public_key_from_x509cert_pem(eidas_link_input):
        x509cert_obj = x509_load_certificate_from_data_bytes(eidas_link_input[0])
        pub_key_expected = x509cert_obj.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        returned_pub_key = get_public_key_from_x509cert_pem(eidas_link_input[0]).public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        assert pub_key_expected == returned_pub_key