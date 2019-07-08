# test_eidas_bridge.py

from eidas_bridge.eidaslink import EIDASLink
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
def test_EIDASLINK_class_bad_types(did, certificate, proof):
    with pytest.raises(TypeError):
        EIDASLink(did, certificate, proof)

@pytest.mark.parametrize("did", dids)
@pytest.mark.parametrize("certificate", certificates)
@pytest.mark.parametrize("proof", proofs)
def test_EIDASLINK_class(did, certificate, proof):
    eidas_link = EIDASLink(did, certificate, proof)
    assert eidas_link._did == did
    assert eidas_link._certificate == certificate
    assert eidas_link._proof == proof