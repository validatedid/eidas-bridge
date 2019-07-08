"""Cryptography functions used by eIDAS Bridge."""

import pysodium

def eidas_hash_byte(b_data: bytes) -> str:
    """ Generates a 256-hash hex string from bytes """
    return pysodium.crypto_hash_sha256(b_data).hex()

def eidas_hash_str(str_data: str) -> str:
    """ Generates a 256-hash hex string from a given text string  """
    return eidas_hash_byte(str_data.encode('utf8'))

def eidas_hash_hex(hex_data: str) -> str:
    """ Generates a 256-hash hex string from a given hex string data """
    return eidas_hash_byte(bytes.fromhex(hex_data))