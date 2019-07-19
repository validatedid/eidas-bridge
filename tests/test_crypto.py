# test_crypto.py

#test_crypto.py
""" Unit test for cryptographic functions from tests/crypto.py file for auxiliary testing purposes """

import pytest
from demo.util.crypto import eidas_crypto_hash_str
from demo.data.common_data import crypto_testdata

@pytest.mark.parametrize("did, expected", crypto_testdata)
def test_eidas_crypto_hash_str(did, expected):
    assert eidas_crypto_hash_str(did) == expected
