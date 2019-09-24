# versioned from https://github.com/WebOfTrustInfo/ld-signatures-python/blob/master/jld_signatures.py
# and https://github.com/decentralized-identity/lds-ecdsa-secp256k1-2019.js/tree/master/packages/lds-ecdsa-secp256k1-2019 

from copy import deepcopy
from datetime import datetime
import pytz
from pyld import jsonld
from eidas_bridge.utils.crypto import eidas_crypto_hash_byte
from eidas_bridge.utils.es256k_jws import sign_jws

def normalize_jsonld(jld_document:str) -> bytes:
    """
    Normalize and hash the json-ld document
    """
    
    options = {'algorithm': 'URDNA2015', 'format': 'application/nquads'}
    normalized = jsonld.normalize(jld_document, options=options)
    normalized_hash = eidas_crypto_hash_byte(b_data=normalized.encode('utf-8'))
    return normalized_hash


def sign(jld_document:str, verification_method:str, private_key:bytes) -> dict:
    """
    Produces a signed JSON-LD document with a Json Web Signature
    """
    
    jld_document = deepcopy(jld_document)
    normalized_jld_hash = normalize_jsonld(jld_document)
    jws_signature = sign_jws(normalized_jld_hash, private_key)

    # returns the proof structure
    return {
        'type': 'EcdsaSecp256k1Signature2019',
        'created': datetime.now(tz=pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'domain': 'example.com',
        'proofPurpose': 'authentication',
        "verificationMethod": verification_method,
        'jws': jws_signature.decode('utf-8')
    }
    

"""
def verify(signed_jld_document, public_key):"""
"""
Verifies the Json Web Signature of a signed JSON-LD Document
"""
"""
signed_jld_document = deepcopy(signed_jld_document)
signature = signed_jld_document.pop('signature')
jws_signature = signature['signatureValue'].encode('utf-8')
normalized_jld_hash = normalize_jsonld(signed_jld_document)

return verify_jws(normalized_jld_hash, jws_signature, public_key)
"""