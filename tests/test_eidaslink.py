# test_eidas_bridge.py

import pytest
from eidas_bridge.eidaslink import EIDASLink
from demo.data.common_data import all_type_dids, all_type_certificates, bad_type_proofs, \
    dids, bad_obj_type_paddings, bad_type_paddings, eidas_link_inputs
from eidas_bridge.utils.crypto import InvalidPaddingException

@pytest.mark.parametrize("did", all_type_dids)
@pytest.mark.parametrize("certificate", all_type_certificates)
@pytest.mark.parametrize("proof", bad_type_proofs)
@pytest.mark.parametrize("padding", bad_obj_type_paddings)
def test_EIDASLINK_class_bad_types(did, certificate, proof, padding):
    with pytest.raises(TypeError):
        EIDASLink(did, certificate, proof, padding)

@pytest.mark.parametrize("did", dids)
@pytest.mark.parametrize("eidas_link_input", eidas_link_inputs)
@pytest.mark.parametrize("padding", bad_type_paddings)
def test_EIDASLINK_class_bad_type_padding(did, eidas_link_input, padding):
    with pytest.raises(InvalidPaddingException):
        EIDASLink(did, eidas_link_input[0], eidas_link_input[1], padding)

@pytest.mark.parametrize("did", dids)
@pytest.mark.parametrize("eidas_link_input", eidas_link_inputs)
def test_EIDASLINK_class(did, eidas_link_input):
    eidas_link = EIDASLink(did, eidas_link_input[0], eidas_link_input[1], eidas_link_input[2])
    assert eidas_link._did == did
    assert eidas_link._x509cert == (eidas_link_input[0]).encode()
    assert eidas_link._proof == bytes.fromhex(eidas_link_input[1])
    assert eidas_link._padding == eidas_link_input[2]