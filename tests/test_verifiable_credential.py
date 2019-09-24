# test_verifiable_credential.py

import pytest
from eidas_bridge.verifiable_credential import VerifiableCredential, EIDASVerifiableCredentialNoIssuerException
from demo.data.common_data import credentials, bad_credentials, test_proof, test_credentials
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
def test_verifiable_credential_no_issuer(credential):
    with pytest.raises(EIDASVerifiableCredentialNoIssuerException):
        VerifiableCredential(credential)

@pytest.mark.parametrize("credential", test_credentials)
def test_add_proof_element(credential):
    vc = VerifiableCredential(credential[0])
    vc._add_element('proof', test_proof)

    str_expected_credential = json.dumps(credential[1], indent=4)
    str_out_credential = vc.to_json()
    assert str_out_credential == str_expected_credential
