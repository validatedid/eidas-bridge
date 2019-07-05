import eidas_bridge

def test_eidas_link_did():
    did = "this is a test DID"
    certificate = "this is a test certificate"
    proof = "this is a proof"
    result =  eidas_bridge.eidas_link_did(did, certificate, proof)
    assert result == ""

def test_eidas_get_service_endpoint_struct():
    storage_endpoint = "http://service_endpoint.sample"
    result = eidas_bridge.eidas_get_service_endpoint_struct(storage_endpoint)
    assert result == ""

def test_eidas_sign_credential():
    json_credential = "{this is a json credential}"
    result = eidas_bridge.eidas_sign_credential(json_credential)
    assert result == ""


def test_eidas_verify_credential():
    json_credential = "{this is a json credential}"
    result = eidas_bridge.eidas_verify_credential(json_credential)
    assert result == "NOT VALID"
