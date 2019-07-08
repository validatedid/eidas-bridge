# test_eidas_bridge.py

from eidas_bridge.eidas_bridge import eidas_link_did, \
    eidas_get_service_endpoint_struct, eidas_sign_credential, eidas_verify_credential
import pytest
import json
from utils.util import bytes_to_b58

dids = [
    "did:sov:55GkHamhTU1ZbTbV2ab9DE"
]

certificates = [
    b"\xd6\x98\x04\x88\xd2-\xc1D\x02\x15\xc9Z\x9bK \x8f\xe0\x8b5\xd0Z$"
]

proofs = [
    b"\xd6\x98\x04\x88\xd2-\xc1D\x02\x15\xc9Z\x9bK \x8f\xe0\x8b5\xd0Z$"
]

all_type_dids = [
    b"\xd6\x98\x04\x88\xd2-\xc1D\x02\x15\xc9Z\x9bK \x8f\xe0\x8b5\xd0Z$",
    "did:sov:55GkHamhTU1ZbTbV2ab9DE",
    0
]

all_type_certificates = [
    b"\xd6\x98\x04\x88\xd2-\xc1D\x02\x15\xc9Z\x9bK \x8f\xe0\x8b5\xd0Z$",
    0,
    ""
]

bad_type_proofs = [
    "this is a proof",
    20
]

endpoints = [
    "http://service_endpoint.sample"
]

bad_type_endpoints = [
    b"\xd6\x98\x04\x88\xd2-\xc1D\x02\x15\xc9Z\x9bK \x8f\xe0\x8b5\xd0Z$",
    0
]

credentials = [
    "{this is a json credential}"
] 

bad_type_credentials = [
    b"\xd6\x98\x04\x88\xd2-\xc1D\x02\x15\xc9Z\x9bK \x8f\xe0\x8b5\xd0Z$",
    0
] 

@pytest.mark.parametrize("did", all_type_dids)
@pytest.mark.parametrize("certificate", all_type_certificates)
@pytest.mark.parametrize("proof", bad_type_proofs)
def test_eidas_link_did_bad_types(did, certificate, proof):
    with pytest.raises(TypeError):
        eidas_link_did(did, certificate, proof)

@pytest.mark.parametrize("did", dids)
@pytest.mark.parametrize("certificate", certificates)
@pytest.mark.parametrize("proof", proofs)
def test_eidas_link_did(did, certificate, proof):
    assert eidas_link_did(did, certificate, proof) == _to_json(did, certificate, proof)

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


def _to_json(did, certificate, proof) -> str:
    """
    Create a JSON representation of the model instance.

    Returns:
        A JSON representation of this message

    """
    return json.dumps(_serialize(did, certificate, proof), indent=2)

def _serialize(did, certificate, proof) -> str:
    """
    Dump current object to a JSON-compatible dictionary.

    Returns:
        dict representation of current EIDASLink

    """
    return {
        "did": did,
        "certificate": bytes_to_b58(certificate),
        "proof": bytes_to_b58(proof)
    }