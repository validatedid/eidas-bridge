# test_eidas_bridge.py
import json, multiprocessing, pytest
from eidas_bridge.eidas_bridge import eidas_get_service_endpoint, eidas_sign_credential, eidas_verify_credential, \
        EIDASNotSupportedException, eidas_load_qec, eidas_get_pubkey
from eidas_bridge.utils.util import timestamp
from demo.data.common_data import all_type_dids, all_type_certificates, bad_type_proofs, \
        dids, bad_type_endpoints, service_endpoints, bad_type_credentials, credentials, did_documents, \
        eidas_data_list, dids, basic_credentials
from demo.util.hub_server import start_hub_server
from eidas_bridge.utils.dbmanager import DBManager, EIDASNotDataCreated
from eidas_bridge.utils.crypto import eidas_load_pkcs12, _load_private_key_from_data, ecdsa_sign
from demo.util.crypto import ecdsa_verify_priv

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
        _check_data_stored(p12_data, p12_password, eidas_data[0])
    
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

def _check_data_stored(p12_data:bytes, p12_password:bytes, did:str):
    # reads the stored data in disk
    dbmanager = DBManager()
    qec = dbmanager.get_qec(did)
    privkey, password = dbmanager.get_key(did)
    # deletes last entry
    dbmanager._delete_last()

    encoded_password = password.encode("utf-8")
    assert encoded_password == p12_password

    # loads key and cert from p12 data
    expected_priv_key, expected_cert = eidas_load_pkcs12(p12_data, encoded_password)
    
    assert qec == expected_cert
    assert _compare_private_keys(privkey, p12_password, expected_priv_key, encoded_password)

@pytest.mark.parametrize("eidas_data", eidas_data_list)
def test_input_parameters_eidas_load_qec(eidas_data):
    p12_data_hex_str = (b'0\x82\x03\xc9\x02\x01\x030\x82\x03\x8f\x06\t*\x86H\x86\xf7\r\x01\x07\x01\xa0\x82\x03\x80\x04\x82\x03|0\x82\x03x0\x82\x02w\x06\t*\x86H\x86\xf7\r\x01\x07\x06\xa0\x82\x02h0\x82\x02d\x02\x01\x000\x82\x02]\x06\t*\x86H\x86\xf7\r\x01\x07\x010\x1c\x06\n*\x86H\x86\xf7\r\x01\x0c\x01\x060\x0e\x04\x08\'?\xfc\xa4]\xbf\x80k\x02\x02\x08\x00\x80\x82\x020}A9N;\x89/j\x8e8\xc57=\x1d!\xae!0\xcd\xaf7}cN>\xcac\xb6nqU\x8c>\x1ff\xce\xe45\xcf\r\xb8~O\xf1\xae\xd5\xde \x0ch\xe1\xe3]\x90\xbc\xa5cBv\xbc\xbf\xc3\x1a\xf2\x91\xa6\x9a\xd1\xac"?\xealH\x06\xf0\xce\xb8\x96s\xc7\xca\x0bK\xaa\xe7+\xa5\xe3\xb7\x82\x07\xfc\x1d%<\x95\x9d:\xff\xed\xc7\x03\xb9\x7f\xa5\xbb\xab\xfd`\x17\x01\x1fp\xe6W\xc7\x88\xde\xa4\xa7\xd2\x8f\xb48m[\xcdl\xb6\xba#0B\x97\xae[\x8d\xf4\x99\xa4\xcb\x94\xea>\x04\xbc\xc7\'\xc2\xc4\xc0b\x01\xe7\xb6O\xfe\xdaA~\xb7\xa8\x8a\x02\x82\x7f\xe9\x1f\xae\x8c\xef=\xf6\x90(\xddK\xe5\xeaB$XC\x84U\\N=ut\xc9\xe5]\xe2\x0b\xe8\x80\xc3\x84G~M\xa8+\xb1\xb0sL\xcb\xb7&\xb4jQM\x8c\x8c\x8b\xbe\xbe7Zghj\x1b\xf5\x00\xe1\x06f.\xbb\xf5\x98\xf8j$\xa2\xc9L\xe1\x08S\xbe\xc2Z\x14f\xb6\xa3\xa2\x8dI\xd1\x07~\x08\x9e\xdf\xd2"\xc9\xaa\xc8a\xc5Q\x89\xac\x91{\x967H]c0\xa2N\xe4\xbe\x14\x18\xe3aC\x88B\x80\r\x84\x90\xcf\xf8\x9c2\xccs\xea~bg\x99OU\x04WU:\xc9\x03\x9e\xfa\x96\x13D\x89}\xed\x92\xc5?G\xf7\xdb\xa3\x0eg;\x01\x93-\x88\xa5;\xc6\xc1:\xe3\x93\xfa\x9a9\xde\xe5:\\\x88\x8a\x92\xf9T\xb4|\xa4\xf3\xecT-\xc0\xa7Y\xf3\x0f\x0c\xb3\x92\x06\t\x9f\x1c\x96\x9c\xf4*\xfc.\x1b7.\xa2\x80\x1b\xd2\xf8DQ\xa4\x86\x13\x16E\x1b%\x90%\xeaO\xf0#\x06\x87\xe0\x8a\xfe\xcc\xb0\xb6F\x08\xb1y\xca\xc8\x92\x0bD\xd6\xd0\xb2\xfd\xa4[[\xe3\xcf\xe2\x9c\x00\x97\xbc\x95\x0f\x8a\xaf\xbb\x8c\xa6\xaa]5\xb3\x01[\xc1a\xe9\x06@\x8a\xbc\xd8]\xba\'&\xd6\xaa_\x9e+c\xfb\x9d\xc6\xbc\xd8\x1d\xe5t\xe8\x9eL@\x80\x99\xeeV\x12\x06\x04a\xaa7J\xbd\xa1\xe3p2_\x9b\xd7\xb6\xdd\x98\xf1kx\x19\x9a\xc8\xdeXP\xa6\x15\xd7\xb5\xc9\xb1N\xefbZ\xb6\x8e\x91\xff\xa2\x877\x84f\xc1\xee\xcd7\x1dZp\xc4\xce\xe3\x1f\xda\x0e\x9fY\xa3\xce\x0b~N\xaa\xe6\x91\xee<\xf0\x13\xa1:\x1a\x0f\xdf\xce%0\x81\xfa\x06\t*\x86H\x86\xf7\r\x01\x07\x01\xa0\x81\xec\x04\x81\xe90\x81\xe60\x81\xe3\x06\x0b*\x86H\x86\xf7\r\x01\x0c\n\x01\x02\xa0\x81\xac0\x81\xa90\x1c\x06\n*\x86H\x86\xf7\r\x01\x0c\x01\x030\x0e\x04\x08\xfa\xe77\x12\xfb\xcbB\xe9\x02\x02\x08\x00\x04\x81\x88(\xde\x9f?\xc3\xcc#f\xb9>\x12\xa1\xd7\xefF\xea\xa3\xd8\x88v%\x1cv\xf8I\xb4K\x1e\xc6q\x85\xe2\x95a\x83*pI@\x13q\x19>\xdb\xce\xb0\x86 \x16n\xce\xc1\xe0cl\xd7_H\xc2\x8c\xac\xdc\xc5<\xb58\xe6\xfa\xfc\xf8\xf5HRH\x83\x17\xd5(\xcf;=z\x12r\x18z\x95\x7fz\xb4\xac\xeb0\xe8\xc4\xb5O\xae>\xa07C>,\xd2\xd3;\xbeQ\xab\xdc\xb0\x01\xd8\x93s\xfchu\xae\xbe\x97%\x19\xb5\xf4\xbc\xb9\x05\x83\xcc)/\xbc\x16e1%0#\x06\t*\x86H\x86\xf7\r\x01\t\x151\x16\x04\x14]F\x8e\xb5\xcd\x8c\r\xb1q\xcd\xf3\x87X\x80\x9f\x04\xac\x95\xeb\xc8010!0\t\x06\x05+\x0e\x03\x02\x1a\x05\x00\x04\x14\x13m\x9f\xe5m\x93^\xb5G\x81q\xf4\x1aN\xf2\x90\xdeb\xb06\x04\x08\xf9\x10\x1c\x1c:f\xca\xb7\x02\x02\x08\x00').hex()
    p12_password = 'passphrase'
    eidas_load_qec(eidas_data[0], p12_data_hex_str, p12_password) 
    _check_data_stored(bytes.fromhex(p12_data_hex_str), p12_password.encode("utf-8"), eidas_data[0])

@pytest.mark.parametrize("did", dids)
def test_get_pubkey_bad_did(did):
    dbmanager = DBManager()

    with pytest.raises(EIDASNotDataCreated):
        dbmanager._get_did_data(did)

@pytest.mark.parametrize("eidas_data", eidas_data_list)
def test_get_pubkey(eidas_data):
    path_to_p12_file = "./demo/data/ECDSAcertificate.p12"
    p12_password = b"passphrase"
    with open(path_to_p12_file, "rb") as p12_file:
        p12_data = p12_file.read()
        eidas_load_qec(eidas_data[0], p12_data, p12_password) 
    
    out_pub_key_json = eidas_get_pubkey(eidas_data[0])
    out_pub_key = json.loads(out_pub_key_json)

    #deletes last entry
    dbmanager = DBManager()
    dbmanager._delete_last()

    assert out_pub_key["publicKeyPem"] == eidas_data[4]

@pytest.mark.parametrize("credential", basic_credentials)
def test_eidas_sign_credential(credential):
    # to keep sure that exists a key loaded in the issuer DB
    path_to_p12_file = "./demo/data/ECDSAcertificate.p12"
    p12_password = b"passphrase"
    did = "did:ebsi:21tDAKCERh95uGgKbJNHYp"

    with open(path_to_p12_file, "rb") as p12_file:
        p12_data = p12_file.read()
        eidas_load_qec(did, p12_data, p12_password) 
    
    out_vc_json = eidas_sign_credential(credential[0])
    out_vc_dict = json.loads(out_vc_json)
    # removes created key because it is dynamically created every time
    del out_vc_dict['proof']['created']
    del out_vc_dict['proof']['jws'] # !!! To be deleted
    out_vc_json = json.dumps(out_vc_dict, indent=4)

    del credential[1]['proof']['created']
    del credential[1]['proof']['jws'] # !!! To be deleted
    expected_vc_json = json.dumps(credential[1], indent=4)

    #deletes last entry
    dbmanager = DBManager()
    dbmanager._delete_last()

    # besides comparing the output value, it is needed to perform a verify signature
    assert out_vc_json == expected_vc_json
