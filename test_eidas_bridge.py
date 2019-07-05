# test_eidas_bridge.py

import eidas_bridge
import pytest

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
        eidas_bridge.eidas_link_did(did, certificate, proof)

@pytest.mark.parametrize("did", dids)
@pytest.mark.parametrize("certificate", certificates)
@pytest.mark.parametrize("proof", proofs)
def test_eidas_link_did(did, certificate, proof):
    result =  eidas_bridge.eidas_link_did(did, certificate, proof)
    assert result == ""

@pytest.mark.parametrize("storage_endpoint", bad_type_endpoints)
def test_eidas_get_service_endpoint_struct_bad_types(storage_endpoint):
    with pytest.raises(TypeError):
        eidas_bridge.eidas_get_service_endpoint_struct(storage_endpoint)

@pytest.mark.parametrize("storage_endpoint", endpoints)
def test_eidas_get_service_endpoint_struct(storage_endpoint):
    result = eidas_bridge.eidas_get_service_endpoint_struct(storage_endpoint)
    assert result == ""

@pytest.mark.parametrize("credential", bad_type_credentials)
def test_eidas_sign_credential_bad_types(credential):
    with pytest.raises(TypeError):
        eidas_bridge.eidas_sign_credential(credential)

@pytest.mark.parametrize("credential", credentials)
def test_eidas_sign_credential(credential):
    result = eidas_bridge.eidas_sign_credential(credential)
    assert result == ""

@pytest.mark.parametrize("credential", bad_type_credentials)
def test_eidas_verify_credential_bad_types(credential):
    with pytest.raises(TypeError):
        eidas_bridge.eidas_verify_credential(credential)

@pytest.mark.parametrize("credential", credentials)
def test_eidas_verify_credential(credential):
    result = eidas_bridge.eidas_verify_credential(credential)
    assert result == "NOT VALID"