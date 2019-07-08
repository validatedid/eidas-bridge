# eidaslink.py
""" Represents an eIDAS Link structure """

from utils.util import check_args, bytes_to_b58
import json

class EIDASProofException(Exception):
    """Error raised when a proof does not match to the signed DID hash."""

class EIDASLink():
    """ Represents an eIDAS Link structure """

    def __init__(self, did, certificate, proof):
        check_args(did, str)
        check_args(certificate, bytes)
        check_args(proof, bytes)

        self._did = did
        self._certificate = certificate
        self._proof = proof
        """ check signarure proof before finishing the object creation """
        self._check_proof()

    def _check_proof(self):
        """ checks that the proof really corresponds to the signed hash of the DID 
        passed as argument, signed with the certificate private key 
        
        Raise EIDASProofException
        """
        # TO DO 
        # check signature
        # result_proof = _check_signature()
        result_proof = self._proof
        if self._proof != result_proof:
            raise EIDASProofException("Proof does not correspond to the certificate signed DID")



    def get_public_key(self) -> bytes:
        """ Returns the certificate public key in bytes format """

        # TODO
        """ extract the public key of the certificate """
        # dummy bytes
        return b"\xd6\x98\x04\x88\xd2-\xc1D\x02\x15\xc9Z\x9bK \x8f\xe0\x8b5\xd0Z$"

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
        return {
            "did": self._did,
            "certificate": bytes_to_b58(self._certificate),
            "proof": bytes_to_b58(self._proof)
        }