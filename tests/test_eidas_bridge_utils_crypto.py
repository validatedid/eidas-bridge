#test_eidas_bridge_utils_crypto.py
""" Unit test for cryptographic functions from eidas_bridge/utils/crypto.py file for eIDAS Library """

import pytest
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from demo.data.common_data import eidas_inputs, bad_obj_type_paddings, paddings, bad_type_paddings, \
    PKCS1v15_PADDING, PSS_PADDING
from eidas_bridge.utils.crypto import x509_load_certificate_from_data_bytes, check_args_padding, \
        InvalidPaddingException, InvalidSignatureException, get_public_key_from_x509cert_obj, \
        get_public_key_from_x509cert_pem, rsa_verify_pss, rsa_verify_pkcs1, rsa_verify
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

@pytest.mark.parametrize("eidas_input", eidas_inputs)
def test_x509_load_certificate_from_data_bytes(eidas_input):
    internal_cert = x509_load_certificate_from_data_bytes((eidas_input[0]).encode())
    expected_cert = x509.load_pem_x509_certificate((eidas_input[0]).encode(), default_backend())
    assert internal_cert == expected_cert

@pytest.mark.parametrize("eidas_input", eidas_inputs)
def test_get_public_key_from_x509cert_obj(eidas_input):
        x509cert_obj = x509_load_certificate_from_data_bytes((eidas_input[0]).encode())
        pub_key_expected = x509cert_obj.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        returned_pub_key = get_public_key_from_x509cert_obj(x509cert_obj).public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        assert pub_key_expected == returned_pub_key

@pytest.mark.parametrize("eidas_input", eidas_inputs)
def test_get_public_key_from_x509cert_pem(eidas_input):
        x509cert_obj = x509_load_certificate_from_data_bytes((eidas_input[0]).encode())
        pub_key_expected = x509cert_obj.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        returned_pub_key = get_public_key_from_x509cert_pem((eidas_input[0]).encode()).public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        assert pub_key_expected == returned_pub_key

@pytest.mark.parametrize("eidas_input", eidas_inputs)
def test_rsa_verify_pss(eidas_input):
        if eidas_input[2] == PSS_PADDING:
                rsa_verify_pss(
                    bytes.fromhex(eidas_input[1]), 
                    eidas_input[3].encode('utf-8'),
                    get_public_key_from_x509cert_pem((eidas_input[0]).encode())
                )
        pass

@pytest.mark.parametrize("eidas_input", eidas_inputs)
def test_rsa_verify_pss_invalid_signature(eidas_input):
        if eidas_input[2] == PSS_PADDING:
                with pytest.raises(InvalidSignatureException):
                        bad_signature = bytes.fromhex('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
                        rsa_verify_pss(bad_signature, eidas_input[3].encode('utf-8'), 
                        get_public_key_from_x509cert_pem((eidas_input[0]).encode()))

@pytest.mark.parametrize("eidas_input", eidas_inputs)
def test_rsa_verify_pkcs1(eidas_input):
        if eidas_input[2] == PKCS1v15_PADDING:
                rsa_verify_pkcs1(bytes.fromhex(eidas_input[1]), eidas_input[3].encode('utf-8'),
                get_public_key_from_x509cert_pem((eidas_input[0]).encode()))
        pass

@pytest.mark.parametrize("eidas_input", eidas_inputs)
def test_rsa_verify_pkcs1_invalid_signature(eidas_input):
        if eidas_input[2] == PKCS1v15_PADDING:
                with pytest.raises(InvalidSignatureException):
                        bad_signature = bytes.fromhex('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
                        rsa_verify_pkcs1(bad_signature, eidas_input[3].encode('utf-8'), 
                        get_public_key_from_x509cert_pem((eidas_input[0]).encode()))

@pytest.mark.parametrize("eidas_input", eidas_inputs)
def test_rsa_verify(eidas_input):
        rsa_verify(
            bytes.fromhex(eidas_input[1]), 
            eidas_input[3].encode('utf-8'),
            get_public_key_from_x509cert_pem((eidas_input[0]).encode()), 
            eidas_input[2]
        )
        pass

@pytest.mark.parametrize("eidas_input", eidas_inputs)
def test_rsa_verify_invalid_signature(eidas_input):
        with pytest.raises(InvalidSignatureException):
                bad_signature = bytes.fromhex('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
                rsa_verify(
                    bad_signature, 
                    eidas_input[3].encode('utf-8'), 
                    get_public_key_from_x509cert_pem((eidas_input[0]).encode()),
                    eidas_input[2]
                )