# test_eidas_bridge.py

import eidas_bridge
import pytest

dids = [
    "did:sov:55GkHamhTU1ZbTbV2ab9DE",
    0,
    ""
]

certificates = [
    "did:sov:55GkHamhTU1ZbTbV2ab9DE",
    0,
    ""
]

proofs = [
    b"\xd6\x98\x04\x88\xd2-\xc1D\x02\x15\xc9Z\x9bK \x8f\xe0\x8b5\xd0Z$",
    "this is a proof",
    20
]

endpoints = [
    "http://service_endpoint.sample",
    0,
    ""
]

credentials = [
    "{this is a json credential}",
    0,
    ""
] 

@pytest.mark.parametrize("did", dids)
@pytest.mark.parametrize("certificate", certificates)
@pytest.mark.parametrize("proof", proofs)
def test_eidas_link_did(did, certificate, proof):
    result =  eidas_bridge.eidas_link_did(did, certificate, proof)
    assert result == ""

@pytest.mark.parametrize("storage_endpoint", endpoints)
def test_eidas_get_service_endpoint_struct(storage_endpoint):
    result = eidas_bridge.eidas_get_service_endpoint_struct(storage_endpoint)
    assert result == ""

@pytest.mark.parametrize("credential", credentials)
def test_eidas_sign_credential(credential):
    result = eidas_bridge.eidas_sign_credential(credential)
    assert result == ""

@pytest.mark.parametrize("credential", credentials)
def test_eidas_verify_credential(credential):
    result = eidas_bridge.eidas_verify_credential(credential)
    assert result == "NOT VALID"
