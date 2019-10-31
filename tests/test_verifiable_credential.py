# test_verifiable_credential.py

import pytest
from eidas_bridge.verifiable_credential import VerifiableCredential, EIDASVerifiableCredentialNoKeyException
from demo.data.common_data import credentials, bad_credentials, test_proof, test_credentials, eidas_data_list, basic_credentials
import json

def test_verifiable_credential_class_bad_types():
    with pytest.raises(TypeError):
        VerifiableCredential(json.dumps(credentials[0]))

@pytest.mark.parametrize("credential", credentials)
def test_verifiable_credential(credential):
    str_credential = json.dumps(credential, indent=4)
    assert VerifiableCredential(credential).to_json() == str_credential

@pytest.mark.parametrize("credential", credentials)
def test_get_issuer_did(credential):
    assert VerifiableCredential(credential).get_issuer_did() == credential['issuer']

@pytest.mark.parametrize("credential", bad_credentials)
def test_verifiable_credential_no_attribute(credential):
    with pytest.raises(EIDASVerifiableCredentialNoKeyException):
        VerifiableCredential(credential)

@pytest.mark.parametrize("credential", test_credentials)
def test_add_proof_element(credential):
    vc = VerifiableCredential(credential[0])
    vc._add_element('proof', test_proof)

    str_expected_credential = json.dumps(credential[1], indent=4)
    str_out_credential = vc.to_json()
    assert str_out_credential == str_expected_credential

@pytest.mark.parametrize("eidas_data", eidas_data_list)
@pytest.mark.parametrize("credential", basic_credentials)
def test_sign_and_add_proof(eidas_data, credential):
    vc = VerifiableCredential(credential[0])
    vc.sign_and_add_proof(eidas_data[2], eidas_data[3].encode("utf-8"))
    # removes created key because it is dynamically created every time
    del vc._verifiable_credential['proof']['created']
    del vc._verifiable_credential['proof']['jws'] # !!! To be deleted
    vc_json = vc.to_json() 

    del credential[1]['proof']['created']
    del credential[1]['proof']['jws'] # !!! To be deleted
    expected_vc_json = json.dumps(credential[1], indent=4)

    assert vc_json == expected_vc_json

