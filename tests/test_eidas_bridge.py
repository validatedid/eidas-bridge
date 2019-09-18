# test_eidas_bridge.py
import json, multiprocessing, pytest
from eidas_bridge.eidas_bridge import eidas_get_service_endpoint, eidas_sign_credential, eidas_verify_credential, \
        EIDASNotSupportedException, eidas_load_qec
from eidas_bridge.utils.util import timestamp
from demo.data.common_data import all_type_dids, all_type_certificates, bad_type_proofs, \
        dids, bad_type_endpoints, service_endpoints, bad_type_credentials, credentials, did_documents, \
        eidas_data_list
from demo.util.hub_server import start_hub_server
from eidas_bridge.utils.dbmanager import DBManager
from eidas_bridge.utils.crypto import eidas_load_pkcs12
from demo.util.crypto import ecdsa_sign, ecdsa_verify_priv, _load_private_key_from_data

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

    # run server process
    hub_server_proc = multiprocessing.Process(target=start_hub_server)
    hub_server_proc.start()

    assert eidas_verify_credential(credential, did_doc) == "VALID"
  
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

@pytest.mark.parametrize("eidas_data", eidas_data_list)
def test_eidas_load_qec(eidas_data):
    path_to_p12_file = "./demo/data/ECDSAcertificate.p12"
    p12_password = b"passphrase"
    with open(path_to_p12_file, "rb") as p12_file:
        p12_data = p12_file.read()
        eidas_load_qec(eidas_data[0], p12_data, p12_password) 
    
    # reads the stored data in disk
    dbmanager = DBManager()
    qec = dbmanager.get_qec(eidas_data[0])
    privkey, password = dbmanager.get_key(eidas_data[0])
    # deletes last entry
    dbmanager._delete_last()

    encoded_password = password.encode("utf-8")
    assert encoded_password == p12_password

    # loads key and cert from p12 data
    expected_priv_key, expected_cert = eidas_load_pkcs12(p12_data, encoded_password)
    
    assert qec == expected_cert
    assert qec == eidas_data[1]
    assert _compare_private_keys(privkey, p12_password, expected_priv_key, encoded_password)

def _compare_private_keys(privkey1:str, pass1:bytes, privkey2:str, pass2:bytes) -> bool:
    #load keys to a Private Key Objetct
    private_key1 = _load_private_key_from_data(privkey1.encode("utf-8"), pass1)
    private_key2 = _load_private_key_from_data(privkey2.encode("utf-8"), pass2)

    #sign some message data
    message = b"This is a sample message"
    outsig1 = ecdsa_sign(message, private_key1)
    outsig2 = ecdsa_sign(message, private_key2)

    # verify each signature with the other key
    ecdsa_verify_priv(private_key2, outsig1, message)
    ecdsa_verify_priv(private_key1, outsig2, message)

    return True