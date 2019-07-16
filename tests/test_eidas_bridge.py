# test_eidas_bridge.py

import pytest
import json
from eidas_bridge.eidas_bridge import eidas_link_did, \
        eidas_get_service_endpoint, eidas_sign_credential, eidas_verify_credential, \
        EIDASNotSupportedException
from eidas_bridge.utils.util import timestamp
from tests.data.common_data import all_type_dids, all_type_certificates, bad_type_proofs, \
        dids, bad_type_endpoints, service_endpoints, bad_type_credentials, credentials, \
        eidas_link_inputs, did_documents

@pytest.mark.parametrize("did", all_type_dids)
@pytest.mark.parametrize("certificate", all_type_certificates)
@pytest.mark.parametrize("proof", bad_type_proofs)
def test_eidas_link_did_bad_types(did, certificate, proof):
    with pytest.raises(TypeError):
        eidas_link_did(did, certificate, proof)

@pytest.mark.parametrize("did", dids)
@pytest.mark.parametrize("eidas_link_input", eidas_link_inputs)
def test_eidas_link_did(did, eidas_link_input):
        eidas_link = eidas_link_did(did, eidas_link_input[0], bytes.fromhex(eidas_link_input[1]), eidas_link_input[2])
        expected = _to_json_eidas_link(did, eidas_link_input[0], bytes.fromhex(eidas_link_input[1]), eidas_link_input[2], get_created_timestamp(eidas_link)) 
        assert eidas_link == expected

@pytest.mark.parametrize("did", all_type_dids)
@pytest.mark.parametrize("storage_endpoint", bad_type_endpoints)
def test_eidas_get_service_endpoint_bad_types(did, storage_endpoint):
    with pytest.raises(TypeError):
        eidas_get_service_endpoint(did, storage_endpoint)

@pytest.mark.parametrize("service_endpoint", service_endpoints)
def test_eidas_get_service_endpoint(service_endpoint):
        eidas_service = eidas_get_service_endpoint(
            service_endpoint[0], # did
            service_endpoint[1] # service endpoint
        ) 
        expected = _to_json_eidas_service(
                service_endpoint[0], # did
                service_endpoint[1] # service endpoint
        )
        assert eidas_service == expected

def test_eidas_sign_credential():
        with pytest.raises(EIDASNotSupportedException):
                eidas_sign_credential(None)

@pytest.mark.parametrize("credential", bad_type_credentials)
def test_eidas_verify_credential_bad_types(credential):
    with pytest.raises(TypeError):
        eidas_verify_credential(credential, "")

@pytest.mark.parametrize("credential", credentials)
@pytest.mark.parametrize("did_doc", did_documents)
def test_eidas_verify_credential(credential, did_doc):
        eidas_verify_credential(json.dumps(credential), json.dumps(did_doc))
        pass

def _to_json_eidas_link(did, x509cert, proof, padding, created) -> str:
    """
    Create a JSON representation of the model instance.

    Returns:
        A JSON representation of this message

    """
    return json.dumps(_serialize_eidas_link(did, x509cert, proof, padding, created), indent=2)

def _serialize_eidas_link(did, x509cert, proof, padding, created) -> str:
    """
    Dump current object to a JSON-compatible dictionary.

    Returns:
        dict representation of current EIDASLink

    """
    return {
            "type": "EidasLink",
            "created": created,
            "did": did,
            "certificate": "{}".format(x509cert.decode()),
            "proof": {
                "type": "RsaSignature2018",
                "padding": padding,
                "signatureValue": proof.hex()
            }
    }

def _to_json_eidas_service(did, service_endpoint) -> str:
    """
    Create a JSON representation of the model instance.

    Returns:
        A JSON representation of this message

    """
    return json.dumps(_serialize_eidas_service(did, service_endpoint), indent=1)

def _serialize_eidas_service(did, service_endpoint) -> str:
    """
    Dump current object to a JSON-compatible dictionary.

    Returns:
        dict representation of current EIDAS Service Endpoint

    """
    return {
            "id": did + "#eidas",
            "type": "EidasService",
            "serviceEndpoint": service_endpoint
            }

def get_created_timestamp(eidas1: str) -> str:
        eidas_parsed = json.loads(eidas1)
        return eidas_parsed["created"]