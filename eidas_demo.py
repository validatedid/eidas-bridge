from eidas_bridge.eidas_bridge import eidas_link_did, \
    eidas_get_service_endpoint_struct, eidas_sign_credential, eidas_verify_credential

from utils.crypto import eidas_hash_byte, eidas_hash_str, eidas_hash_hex


dids = [
    "did:sov:55GkHamhTU1ZbTbV2ab9DE"
]

certificates = [
    b"\xd6\x98\x04\x88\xd2-\xc1D\x02\x15\xc9Z\x9bK \x8f\xe0\x8b5\xd0Z$"
]

proofs = [
    b"\xd6\x98\x04\x88\xd2-\xc1D\x02\x15\xc9Z\x9bK \x8f\xe0\x8b5\xd0Z$"
]

endpoints = [
    "http://service_endpoint.sample"
]

credentials = [
    "{this is a json credential}"
] 

def basic_demo():
    """ Initial Demo: very basic """
    print("--- INIT EIDAS DEMO ---\n\r")

    print("1.- calling eidas link did ")
    print (eidas_link_did(dids[0], certificates[0], proofs[0]))

    print("\n2.- calling eidas get service endpoint struct ")
    print (eidas_get_service_endpoint_struct(endpoints[0]))

    print("\n3.- calling eidas sign credential ")
    print (eidas_sign_credential(credentials[0]))

    print("\n4.- calling eidas verify credential ")
    print (eidas_verify_credential(credentials[0]))

    print("\n--- END EIDAS DEMO ---")

def hash_byte(did):
    print("Input data BYTES:\t" + did.hex())
    print("Output data BYTES:\t" + eidas_hash_byte(did) + "\n")

def hash_str(did):
    print("Input data STR:\t\t" + did)
    print("Output data STR:\t" + eidas_hash_str(did) + "\n")

def hash_hex(did):
    print("Input data HEX STR:\t" + did)
    print("Output data HEX STR:\t" + eidas_hash_hex(did) + "\n")

def test_suite_hash():
    hash_byte(b'PI')
    hash_str("PI")
    hash_str("")
    hash_str(" ")
    hash_str("a")
    hash_str("0")
    hash_str("did:sov:")
    hash_str("55GkHamhTU1ZbTbV2ab9DE")
    hash_str("did:sov:55GkHamhTU1ZbTbV2ab9DE")
    hash_str("did:test:abcdefghijkl")
    hash_hex('fffe00005000000049000000')

if __name__ == '__main__':
    #basic_demo()
    test_suite_hash()