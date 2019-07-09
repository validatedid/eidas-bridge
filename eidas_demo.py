from eidas_bridge.eidas_bridge import eidas_link_did, \
    eidas_get_service_endpoint_struct, eidas_sign_credential, eidas_verify_credential
from utils.crypto import eidas_hash_byte, eidas_hash_str, eidas_hash_hex,  \
    create_selfsigned_x509_certificate, store_rsa_key_and_x509cert_to_disk, \
    get_public_key_from_rsakey_str, x509_get_certificate_from_obj_str, \
    print_rsa_key, print_x509cert, eidas_crypto_hash_byte, eidas_crypto_hash_str, \
    eidas_crypto_hash_hex
from tests.data.common_data import dids, x509certs, proofs, endpoints, credentials

def basic_demo():
    """ Initial Demo: very basic """
    print("--- INIT EIDAS DEMO ---\n\r")

    print("1.- calling eidas link did ")
    print (eidas_link_did(dids[0], x509certs[0], proofs[0]))

    print("\n2.- calling eidas get service endpoint struct ")
    print (eidas_get_service_endpoint_struct(endpoints[0]))

    print("\n3.- calling eidas sign credential ")
    print (eidas_sign_credential(credentials[0]))

    print("\n4.- calling eidas verify credential ")
    print (eidas_verify_credential(credentials[0]))

    print("\n--- END EIDAS DEMO ---")

""""""""""""""""""
""" HASH TESTS """
""""""""""""""""""
def hash_byte(did):
    print("Input data BYTES:\t" + did.hex())
    print("Output data BYTES:\t" + eidas_hash_byte(did) + "\n")

def hash_str(did):
    print("Input data STR:\t\t" + did)
    print("Output data STR:\t" + eidas_hash_str(did) + "\n")

def hash_hex(did):
    print("Input data HEX STR:\t" + did)
    print("Output data HEX STR:\t" + eidas_hash_hex(did) + "\n")

def crypto_hash_byte(did):
    print("Input data BYTES:\t" + did.hex())
    print("Output data BYTES:\t" + eidas_crypto_hash_byte(did) + "\n")

def crypto_hash_str(did):
    print("Input data STR:\t\t" + did)
    print("Output data STR:\t" + eidas_crypto_hash_str(did) + "\n")

def crypto_hash_hex(did):
    print("Input data HEX STR:\t" + did)
    print("Output data HEX STR:\t" + eidas_crypto_hash_hex(did) + "\n")

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

def test_suite_crypto_hash():
    crypto_hash_byte(b'PI')
    crypto_hash_str("PI")
    crypto_hash_str("")
    crypto_hash_str(" ")
    crypto_hash_str("a")
    crypto_hash_str("0")
    crypto_hash_str("did:sov:")
    crypto_hash_str("55GkHamhTU1ZbTbV2ab9DE")
    crypto_hash_str("did:sov:55GkHamhTU1ZbTbV2ab9DE")
    crypto_hash_str("did:test:abcdefghijkl")
    crypto_hash_hex('fffe00005000000049000000')

""""""""""""""""""""""""""""""
""" RSA CRYPTO TEST SUITE  """
""""""""""""""""""""""""""""""
def test_generate_x509cert_and_key_and_store_to_disk(path_to_file):
    # create rsa key and x509 certificate
    rsa_key, x509cert = create_selfsigned_x509_certificate(2048, u'ES', u'TEST_STATE',
    u'TEST_CITY', u'CA_ACME', u'mysite.com',365)

    #store key object and x509 certificate to disk in PEM files
    store_rsa_key_and_x509cert_to_disk(rsa_key, path_to_file + "rsakey.pem", 
        x509cert, path_to_file + "x509cert.pem")

    # print rsa key and x509 certificate
    print("RSA PUB KEY: \n")
    print_rsa_key(rsa_key)
    print ("\nX509 CERTIFICATE: \n")
    print_x509cert(x509cert)

""""""""""""
""" MAIN """
""""""""""""
if __name__ == '__main__':
    basic_demo()
    #test_suite_hash()
    #test_suite_crypto_hash()
    #test_generate_x509cert_and_key_and_store_to_disk("./tests/data/tmp/")