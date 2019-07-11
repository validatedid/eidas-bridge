# eidaslink.py
""" Represents an eIDAS Link structure """

from utils.util import check_args, bytes_to_b58
from utils.crypto import eidas_crypto_hash_str, get_public_key_from_x509cert_obj, \
    x509_load_certificate_from_data_bytes, rsa_verify, x509_get_PEM_certificate_from_obj
import json

class EIDASProofException(Exception):
    """Error raised when a proof does not match to the signed DID hash."""

class EIDASLink():
    """ Represents an eIDAS Link structure """

    def __init__(self, did, x509cert, proof, padding):
        check_args(did, str)
        check_args(x509cert, bytes)
        check_args(proof, bytes)

        self._did = did
        self._x509cert = x509_load_certificate_from_data_bytes(x509cert)
        self._proof = proof
        self._padding=padding

        """ check signarure proof before finishing the object creation """
        self._check_proof()

    def _check_proof(self):
        """ checks that the proof really corresponds to the signed hash of the DID 
        passed as argument, signed with the certificate private key 
        
        Raise EIDASProofException (at the moment InvalidSignature)
        """
        rsa_verify(self._proof, self._did.encode('utf-8'), self._get_public_key(), self._padding)
        
    def _get_public_key(self) -> bytes:
        """ Returns the x509 certificate public key """
        return get_public_key_from_x509cert_obj(self._x509cert)

    def to_json(self) -> str:
        """
        Create a JSON representation of the model instance.

        Returns:
            A JSON representation of this message

        """
        return json.dumps(self.serialize(), indent=2)

    def serialize(self) -> str:
        """
        Dump current object to a JSON-compatible dictionary.

        Returns:
            dict representation of current EIDASLink

        """
        _cert = x509_get_PEM_certificate_from_obj(self._x509cert)
        
        return {
            "did": self._did,
            "certificate": "{}".format(_cert.decode()),
            "proof": self._proof.hex()
        }