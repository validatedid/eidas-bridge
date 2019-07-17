# eidas_service.py
""" Represents an eIDAS Service Endpoint structure """

from .utils.util import check_args, clean_did
import json

class EIDASService():
    """ Represents an eIDAS Service Endpoint structure """

    EIDAS_SERVICE_TYPE = "EidasService"
    EIDAS_SERVICE_FRAGMENT = "#eidas"

    def __init__(self, did, endpoint):
        check_args(did, str)
        check_args(endpoint, str)

        # remove all possible delimiters '#', ';', '?'
        self._did = clean_did(did)
        self._endpoint = endpoint
    
    @classmethod
    def from_json(cls, eidas_service_as_json: str) -> 'EIDASService':
        eidas_str = json.loads(eidas_service_as_json)
        return cls(
            did=clean_did(eidas_str['did']), 
            endpoint=eidas_str['serviceEndpoint']
        )

    def get_endpoint(self) -> str:
        return self._endpoint

    def to_json(self) -> str:
            """
            Create a JSON representation of the model instance.

            Returns:
                A JSON representation of this message

            """
            return json.dumps(self._serialize(), indent=1)

    def _serialize(self) -> str:
        """
        Dump current object to a JSON-compatible dictionary.

        Returns: 
            dict representation of current eIDAS Service Endpoint
        """
        return {
            "id": self._did + EIDASService.EIDAS_SERVICE_FRAGMENT,
            "type": EIDASService.EIDAS_SERVICE_TYPE,
            "serviceEndpoint": self._endpoint
            }
    
    def get_eidas_link_did(self) -> str:
        """ Retrieves a json structure that represents an 
            eIDAS Link DID using the eIDAS Service Endpoint 
        """
        # retrieves the json eidas structure
        # TO DO
        return json.dumps(
            {
                "type": "EidasLink",
                "created": "2019-07-15 16:06:50.454871+00:00",
                "did": "did:sov:55GkHamhTU1ZbTbV2ab9DE",
                "certificate": "-----BEGIN CERTIFICATE-----\nMIIDYDCCAkigAwIBAgIUI63ffVceaNc1kN9O0q/4jSjbkU0wDQYJKoZIhvcNAQEL\nBQAwXTELMAkGA1UEBhMCRVMxEzARBgNVBAgMClRFU1RfU1RBVEUxEjAQBgNVBAcM\nCVRFU1RfQ0lUWTEQMA4GA1UECgwHQ0FfQUNNRTETMBEGA1UEAwwKbXlzaXRlLmNv\nbTAeFw0xOTA3MDkxNDA3MjBaFw0yMDA3MDgxNDA3MjBaMF0xCzAJBgNVBAYTAkVT\nMRMwEQYDVQQIDApURVNUX1NUQVRFMRIwEAYDVQQHDAlURVNUX0NJVFkxEDAOBgNV\nBAoMB0NBX0FDTUUxEzARBgNVBAMMCm15c2l0ZS5jb20wggEiMA0GCSqGSIb3DQEB\nAQUAA4IBDwAwggEKAoIBAQDm6RhyIeFZHn4bGQ/2UQ+aflczCo3Ej04LJXfiIU1Q\nt7xRq3e+uh7nTLffnS7fj/ZZBBREmR/D/SJBTlxv7WQEbscV/pf2LoZLjoC4M4ye\n43lUHRmWsm4J50tu9zcSheqXCRyAK/Ai6RUBy86NKXMFTUp/ONxS0BxJg8GU03Xd\nXGnYzdmZZXGDnublGYq03gD/cZYguS7/HS8v/MckdmjYPTy2syGL9unYkjWn7vig\niaDc2leAM4agKB6PODJSFla15HLoqskKX1SgtLJUHxu/FOo6hYdCt+GxpV1xhl/r\nEf3/SFeTZrJgL11m5ABDli2zAmCn4bjBNnNcXWy5QV0pAgMBAAGjGDAWMBQGA1Ud\nEQQNMAuCCWxvY2FsaG9zdDANBgkqhkiG9w0BAQsFAAOCAQEAYPUn0TzGyn438++1\nV2jMHC653C8tn3vVF5nTT7Td+ihc+KaaNDYsgyY2JpBIMRwlNgoNU0Da3P/9ZDn3\nlFJElUg8WpWPvpXtbS4udqn6UcfT9mFJtkzKg3CK5i50GRCabV9FPbY1bzYtUbY+\nEntXtI2h0dxcgzgOw6pkXFB3O7ZbbshpqWTlHtTtbxxrOFq0zcpyS92G+NTF6ASS\nhXcIf90du/mBWd2dinF/w2nkRAWfGBy8bGnUSJ93rPVwLjI0PDeHh7+PSQ+3X6mG\n5DI9EmzEC7esW6wJbhgiOYXLavAOmLfI0yq/z8SZMvFYwBE69VuGfPSj/u4nIhA5\nK0Qgnw==\n-----END CERTIFICATE-----\n",
                "proof": {
                    "type": "RsaSignature2018",
                    "padding": "PKCS1-v1_5",
                    "signatureValue": "b0c86e06345f1b1b8b50696b5b42458699359e7dde13f535d7598db06891ccd7f4558f8262e23d8825cb65d0f16c72e53f93db7aa51b0831365db2dc8bbefc17d2c535646122ee1e448853044eeb83ffa944fac27e461ed41aa0f9d2079f49b60c88413fcedb287886094a831c79979b9323eac8fdabc1447facdd629d5533d6bc3f1a6a4ba4e420b7733b8617fe15f4f7a9ec81c0ae5b312dab6634082b29450bb77c19cda733719ecc8d758ec7988e39ff1f23dc5cf023156a82f1a73aaf2860d19dc64b452b4b15aa651d8845dbef97f07e3021babd5bdab3b353de271f0c3f95c29087f332d912a684560cad91e097a8978f42e8587b6c034e58ebbe1175"
                }
            }, indent=2)
