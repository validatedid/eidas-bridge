# test_verifiable_credential.py

import pytest
from eidas_bridge.verifiable_credential import VerifiableCredential
from tests.data.common_data import credentials
import json

def test_verifiable_credential_class_bad_types():
    with pytest.raises(TypeError):
        VerifiableCredential(credentials[0])

@pytest.mark.parametrize("credential", credentials)
def test_verifiable_credential(credential):
    str_credential = json.dumps(credential, indent=4)
    assert VerifiableCredential(str_credential).to_json() == str_credential
