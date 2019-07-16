# test_verifiable_credential.py

import pytest
from eidas_bridge.verifiable_credential import VerifiableCredential, EIDASVerifiableCredentialNoIssuerException
from tests.data.common_data import credentials, bad_credentials
import json

def test_verifiable_credential_class_bad_types():
    with pytest.raises(TypeError):
        VerifiableCredential(credentials[0])

@pytest.mark.parametrize("credential", credentials)
def test_verifiable_credential(credential):
    str_credential = json.dumps(credential, indent=4)
    assert VerifiableCredential(str_credential).to_json() == str_credential

@pytest.mark.parametrize("credential", credentials)
def test_get_issuer_did(credential):
    assert VerifiableCredential(json.dumps(credential)).get_issuer_did() == credential['issuer']

@pytest.mark.parametrize("credential", bad_credentials)
def test_verifiable_credential_no_issuer(credential):
    with pytest.raises(EIDASVerifiableCredentialNoIssuerException):
        VerifiableCredential(json.dumps(credential))
