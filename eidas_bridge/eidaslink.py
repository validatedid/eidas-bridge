# eidaslink.py
""" Represents an eIDAS Link structure """

from .utils.util import check_args, timestamp
from .utils.crypto import rsa_verify, check_args_padding, get_public_key_from_x509cert_pem
import json

class EIDASProofException(Exception):
    """Error raised when a proof does not match to the signed DID hash."""

class EIDASLink():
    """ Represents an eIDAS Link structure """

    def __init__(self, did, x509cert, proof, padding):
        check_args(did, str)
        check_args(x509cert, bytes)
        check_args(proof, bytes)
        check_args_padding(padding, str)

        self._did = did
        self._x509cert = x509cert
        self._proof = proof
        self._padding = padding

        """ check signarure proof before finishing the object creation """
        self._check_proof()
    
    @classmethod
    def from_json(cls, eidaslink_as_json: str) -> 'EIDASLink':
        eidas_str = json.loads(eidaslink_as_json)
        return cls(
            did=eidas_str['did'], 
            x509cert=eidas_str['certificate'].encode(),
            proof=bytes.fromhex(eidas_str['proof']['signatureValue']),
            padding=eidas_str['proof']['padding']
        )

    def _check_proof(self):
        """ checks that the proof really corresponds to the signed hash of the DID 
        passed as argument, signed with the certificate private key 
        
        Raise EIDASProofException (at the moment InvalidSignature)
        """
        rsa_verify(self._proof, self._did.encode('utf-8'), self._get_public_key(), self._padding)
        
    def _get_public_key(self) -> bytes:
        """ Returns the x509 certificate public key """
        return get_public_key_from_x509cert_pem(self._x509cert)

    def to_json(self) -> str:
        """
        Create a JSON representation of the model instance.

        Returns:
            A JSON representation of this message

        """
        return json.dumps(self._serialize(), indent=2)

    def _serialize(self) -> str:
        """
        Dump current object to a JSON-compatible dictionary.

        Returns: 
            dict representation of current EIDASLink
        """
        return {
            "type": "EidasLink",
            "created": timestamp(),
            "did": self._did,
            "certificate": "{}".format(self._x509cert.decode()),
            "proof": {
                "type": "RsaSignature2018",
                "padding": self._padding,
                "signatureValue": self._proof.hex()
            }
        }