# test_crypto.py

from utils.crypto import eidas_hash_str
import pytest

testdata = [
    ("","e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    (" ","36a9e7f1c95b82ffb99743e0c5c4ce95d83c9a430aac59f84ef3cbfab6145068"),
    ("a","ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"),
    ("0","5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9"),
    ("did:sov:", "97b40a411bf0e69968c6a0280c88f0d4f170245522d2d07c0cc39ffeffeb7bb2"),
    ("55GkHamhTU1ZbTbV2ab9DE", "9f4fc75928e784dbe2e5a33500aaa08a11906b02ef38309bf23208dca4452ef8"),
    ("did:sov:55GkHamhTU1ZbTbV2ab9DE","32eaebf15929b44167130a124c73b4652f122b9fc92ef5bde91a32f70c2bf049"),
    ("did:test:abcdefghijkl","eff857db6f037dec456ab0802998313059731f39a3f45b72413af30610f79f8c")
]

@pytest.mark.parametrize("did, expected", testdata)
def test_eidas_hash_str(did, expected):
    assert eidas_hash_str(did) == expected
