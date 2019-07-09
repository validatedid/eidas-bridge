# test_eidas_bridge.py

import pytest
import json
from eidas_bridge.eidas_bridge import eidas_link_did, \
    eidas_get_service_endpoint_struct, eidas_sign_credential, eidas_verify_credential
from utils.util import bytes_to_b58
from utils.crypto import x509_get_certificate_from_obj_str
from tests.data.common_data import all_type_dids, all_type_certificates, bad_type_proofs, \
    dids, x509certs, proofs, bad_type_endpoints, endpoints, bad_type_credentials, credentials

@pytest.mark.parametrize("did", all_type_dids)
@pytest.mark.parametrize("certificate", all_type_certificates)
@pytest.mark.parametrize("proof", bad_type_proofs)
def test_eidas_link_did_bad_types(did, certificate, proof):
    with pytest.raises(TypeError):
        eidas_link_did(did, certificate, proof)

@pytest.mark.parametrize("did", dids)
@pytest.mark.parametrize("x509cert", x509certs)
@pytest.mark.parametrize("proof", proofs)
def test_eidas_link_did(did, x509cert, proof):
    assert eidas_link_did(did, x509cert, proof) == _to_json(did, x509cert, proof)

@pytest.mark.parametrize("storage_endpoint", bad_type_endpoints)
def test_eidas_get_service_endpoint_struct_bad_types(storage_endpoint):
    with pytest.raises(TypeError):
        eidas_get_service_endpoint_struct(storage_endpoint)

@pytest.mark.parametrize("storage_endpoint", endpoints)
def test_eidas_get_service_endpoint_struct(storage_endpoint):
    result = eidas_get_service_endpoint_struct(storage_endpoint)
    assert result == ""

@pytest.mark.parametrize("credential", bad_type_credentials)
def test_eidas_sign_credential_bad_types(credential):
    with pytest.raises(TypeError):
        eidas_sign_credential(credential)

@pytest.mark.parametrize("credential", credentials)
def test_eidas_sign_credential(credential):
    result = eidas_sign_credential(credential)
    assert result == ""

@pytest.mark.parametrize("credential", bad_type_credentials)
def test_eidas_verify_credential_bad_types(credential):
    with pytest.raises(TypeError):
        eidas_verify_credential(credential)

@pytest.mark.parametrize("credential", credentials)
def test_eidas_verify_credential(credential):
    result = eidas_verify_credential(credential)
    assert result == "NOT VALID"

def _to_json(did, x509cert, proof) -> str:
    """
    Create a JSON representation of the model instance.

    Returns:
        A JSON representation of this message

    """
    return json.dumps(_serialize(did, x509cert, proof), indent=2)

def _serialize(did, x509cert, proof) -> str:
    """
    Dump current object to a JSON-compatible dictionary.

    Returns:
        dict representation of current EIDASLink

    """
    return {
        "did": did,
        "certificate": "{}".format(x509cert.decode()),
        "proof": bytes_to_b58(proof)
    }