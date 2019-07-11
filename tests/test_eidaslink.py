# test_eidas_bridge.py

import pytest
from eidas_bridge.eidaslink import EIDASLink
from tests.data.common_data import all_type_dids, all_type_certificates, bad_type_proofs, \
    dids, x509certs, proofs, bad_obj_type_paddings, bad_type_paddings, paddings
from eidas_bridge.utils.crypto import InvalidPaddingException

@pytest.mark.parametrize("did", all_type_dids)
@pytest.mark.parametrize("certificate", all_type_certificates)
@pytest.mark.parametrize("proof", bad_type_proofs)
@pytest.mark.parametrize("padding", bad_obj_type_paddings)
def test_EIDASLINK_class_bad_types(did, certificate, proof, padding):
    with pytest.raises(TypeError):
        EIDASLink(did, certificate, proof, padding)

@pytest.mark.parametrize("did", dids)
@pytest.mark.parametrize("x509cert", x509certs)
@pytest.mark.parametrize("proof", proofs)
@pytest.mark.parametrize("padding", paddings)
def test_EIDASLINK_class(did, x509cert, proof, padding):
    eidas_link = EIDASLink(did, x509cert, bytes.fromhex(proof), padding)
    assert eidas_link._did == did
    assert eidas_link._x509cert == x509cert
    assert eidas_link._proof == bytes.fromhex(proof)
    assert eidas_link._padding == padding

@pytest.mark.parametrize("did", dids)
@pytest.mark.parametrize("x509cert", x509certs)
@pytest.mark.parametrize("proof", proofs)
@pytest.mark.parametrize("padding", bad_type_paddings)
def test_EIDASLINK_class_bad_type_padding(did, x509cert, proof, padding):
    with pytest.raises(InvalidPaddingException):
        EIDASLink(did, x509cert, bytes.fromhex(proof), padding)