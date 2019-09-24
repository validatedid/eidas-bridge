# versioned from https://github.com/WebOfTrustInfo/ld-signatures-python/blob/master/jws.py
# and https://github.com/decentralized-identity/lds-ecdsa-secp256k1-2019.js/tree/master/packages/es256k-jws-ts 

import base64
import json
from eidas_bridge.utils.crypto import ecdsa_sign

def b64safe_encode(payload):
    """
    b64 url safe encoding with the padding removed.
    """
    return base64.urlsafe_b64encode(payload).rstrip(b'=')


def b64safe_decode(payload):
    """
    b64 url safe decoding with the padding added.
    """
    return base64.urlsafe_b64decode(payload + b'=' * (4 - len(payload) % 4))


def normalize_json(payload):
    # TODO: Document why the json is normalized this way
    return json.dumps(payload,
                      separators=(',', ':'),
                      sort_keys=True).encode('utf-8')


def sign_jws(payload, private_key):
    # Produce a JWS Unencoded Payload per https://tools.ietf.org/html/rfc7797#section-6 
    header = {
        'alg': 'ES256K', 
        'b64': False, 
        'crit': ['b64']
    }
    normalized_json = normalize_json(header)
    encoded_header = b64safe_encode(normalized_json)
    prepared_payload = b'.'.join([encoded_header, payload])

    signature = ecdsa_sign(prepared_payload, private_key)
    encoded_signature = b64safe_encode(signature)
    jws_signature = b'..'.join([encoded_header, encoded_signature])

    return jws_signature

"""
def verify_jws(payload, jws_signature, public_key):
    # remove the encoded header from the signature
    encoded_header, encoded_signature = jws_signature.split(b'..')
    signature = b64safe_decode(encoded_signature)
    payload = b'.'.join([encoded_header, payload])
    return verify_rs256(payload, signature, public_key)
"""