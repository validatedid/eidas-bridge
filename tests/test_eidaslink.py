# test_eidas_bridge.py

import pytest
from eidas_bridge.eidaslink import EIDASLink
from tests.data.common_data import all_type_dids, all_type_certificates, bad_type_proofs, \
    dids, x509certs, proofs
from utils.crypto import x509_load_certificate_from_data_bytes, PSS_PADDING

@pytest.mark.parametrize("did", all_type_dids)
@pytest.mark.parametrize("certificate", all_type_certificates)
@pytest.mark.parametrize("proof", bad_type_proofs)
def test_EIDASLINK_class_bad_types(did, certificate, proof):
    with pytest.raises(TypeError):
        EIDASLink(did, certificate, proof)

@pytest.mark.parametrize("did", dids)
@pytest.mark.parametrize("x509cert", x509certs)
@pytest.mark.parametrize("proof", proofs)
def test_EIDASLINK_class(did, x509cert, proof):
    eidas_link = EIDASLink(did, x509cert, bytes.fromhex(proof), PSS_PADDING)
    assert eidas_link._did == did
    assert eidas_link._x509cert == x509_load_certificate_from_data_bytes(x509cert)
    assert eidas_link._proof == bytes.fromhex(proof)