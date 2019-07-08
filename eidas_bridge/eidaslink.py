# eidaslink.py
""" Represents an eIDAS Link structure """

from utils.util import check_args

class EIDASLink():
    """ Represents an eIDAS Link structure """

    def __init__(self, did, certificate, proof):
        check_args(did, str)
        check_args(certificate, bytes)
        check_args(proof, bytes)

        self._did = did
        self._certificate = certificate
        self._proof = proof

    def get_public_key(self) -> bytes:
        """ Returns the certificate public key in bytes format """

        # TODO
        """ extract the public key of the certificate """
        # dummy bytes
        return b"\xd6\x98\x04\x88\xd2-\xc1D\x02\x15\xc9Z\x9bK \x8f\xe0\x8b5\xd0Z$"

    