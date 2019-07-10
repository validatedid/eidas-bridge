from eidas_bridge.eidas_bridge import eidas_link_did, \
    eidas_get_service_endpoint_struct, eidas_sign_credential, eidas_verify_credential
from utils.crypto import create_selfsigned_x509_certificate, store_rsa_key_and_x509cert_to_disk, \
    get_public_key_from_rsakey_str, print_rsa_pub_key, InvalidSignatureException, \
    print_x509cert, eidas_crypto_hash_byte, eidas_crypto_hash_str, \
    eidas_crypto_hash_hex, rsa_sign_pss, rsa_verify_pss, rsa_load_private_key_from_file, \
    x509_load_certificate_from_file, x509_get_PEM_certificate_from_obj, print_rsa_priv_key
from tests.data.common_data import dids, x509certs, proofs, endpoints, credentials
from tests.util import bcolors

""""""""""""""""""""""""
""" EIDAS BRIDGE TESTS """
""""""""""""""""""""""""

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

def test_eidas_link_did(path_to_key_file, input_password, 
    path_to_cert_file, did):
    #load key
    rsa_priv_key = rsa_load_private_key_from_file(path_to_key_file, input_password)

    #rsa signature with PSS padding
    proof = rsa_sign_pss(did.encode('utf-8'), rsa_priv_key)
    print("Signature: " + proof.hex())

    #load certificate and convert it to a PEM byte data
    x509cert = x509_load_certificate_from_file(path_to_cert_file)
    pem_cert_data = x509_get_PEM_certificate_from_obj(x509cert)

    #create an eIDAS Link DID structure and print to stdout
    print(eidas_link_did(did, pem_cert_data, proof))

""""""""""""""""""
""" HASH TESTS """
""""""""""""""""""
def crypto_hash_byte(did):
    print("Input data BYTES:\t" + did.hex())
    print("Output data BYTES:\t" + eidas_crypto_hash_byte(did) + "\n")

def crypto_hash_str(did):
    print("Input data STR:\t\t" + did)
    print("Output data STR:\t" + eidas_crypto_hash_str(did) + "\n")

def crypto_hash_hex(did):
    print("Input data HEX STR:\t" + did)
    print("Output data HEX STR:\t" + eidas_crypto_hash_hex(did) + "\n")

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
def test_generate_x509cert_and_key_and_store_to_disk(path_to_dir, input_password, bprint):
    # create rsa key and x509 certificate
    rsa_key, x509cert = create_selfsigned_x509_certificate(2048, u'ES', u'TEST_STATE',
    u'TEST_CITY', u'CA_ACME', u'mysite.com',365)

    #store key object and x509 certificate to disk in PEM files
    store_rsa_key_and_x509cert_to_disk(rsa_key, path_to_dir + "rsakey.pem", input_password,
        x509cert, path_to_dir + "x509cert.pem")

    # print rsa key and x509 certificate
    if bprint:
        _print_certificate(x509cert)
        _print_priv_key(rsa_key, input_password)
        _print_pub_key(x509cert.public_key())

def test_sign_and_verify(path_to_key_file, input_password, message, bprint):
    #load key
    rsa_priv_key = rsa_load_private_key_from_file(path_to_key_file, input_password)

    #rsa signature with PSS padding
    signature = rsa_sign_pss(message.encode('utf-8'), rsa_priv_key)
    if bprint:
        _print_signature(signature)
        _print_pub_key(rsa_priv_key.public_key())

    #rsa validation with the public key
    _verify_and_print_validation(signature, message, rsa_priv_key.public_key())

def test_sign_from_file_verify_from_cert_file(path_to_key_file, input_password, 
    path_to_cert_file, message, bprint):
    #load key
    rsa_priv_key = rsa_load_private_key_from_file(path_to_key_file, input_password)

    #rsa signature with PSS padding
    signature = rsa_sign_pss(message.encode('utf-8'), rsa_priv_key)
    if bprint:
        _print_signature(signature)

    #load certificate and convert it to a PEM byte data
    x509cert = x509_load_certificate_from_file(path_to_cert_file)
   
    if bprint:
        _print_certificate(x509cert)
        _print_pub_key(x509cert.public_key())
    
    #rsa validation with the public key from the loaded certificate
    _verify_and_print_validation(signature, message, x509cert.public_key())

def verify_signature_from_cert_file(path_to_cert_file, message, signature, bprint):
    #load certificate and convert it to a PEM byte data
    x509cert = x509_load_certificate_from_file(path_to_cert_file)

    if bprint:
        _print_certificate(x509cert)
        _print_pub_key(x509cert.public_key())

    #rsa validation with the public key from the loaded certificate
    _verify_and_print_validation(signature, message, x509cert.public_key())

def test_verify_signature_from_cert_file_loop(path_to_cert_file, message, proofs, bprint):
    for signature in proofs:
        verify_signature_from_cert_file(path_to_cert_file, message, bytes.fromhex(signature), bprint)

def crypto_suite_test(tests_to_execute, path_to_dir, path_to_key_file, input_password, 
    path_to_cert_file, message, proofs, bprint):
    
    if tests_to_execute[0]:
        print("CRYPTO TEST 1: Generate x509 certificate and RSA Key and store to disk:\n")
        test_generate_x509cert_and_key_and_store_to_disk(path_to_dir, input_password, bprint)
    if tests_to_execute[1]:
        print("\nCRYPTO TEST 2: Sign a message with a RSA Key loaded from file and Verify the signature with the correspondent public key:\n")
        test_sign_and_verify(path_to_key_file, input_password, message, bprint)
    if tests_to_execute[2]:
        print("\nCRYPTO TEST 3: Sign a message with a RSA Key loaded from file and Verify the signature with the certificate public key loaded from a file:\n")
        test_sign_from_file_verify_from_cert_file(path_to_key_file, input_password, 
        path_to_cert_file, message, bprint)
    if tests_to_execute[3]:
        print("\nCRYPTO TEST 4: Verifies signatures passed as a list and getting the public key from a certificate stores in disk:\n")
        test_verify_signature_from_cert_file_loop(path_to_cert_file, message, proofs, bprint)

""""""""""""""""""""""""
""" AUX FUNCTIONS    """
""""""""""""""""""""""""
def _verify_and_print_validation(signature, message, pub_key):
    #rsa validation with the public key from the loaded certificate
    try:
        rsa_verify_pss(signature, message.encode('utf-8'), pub_key)
        print("Signature validation: " + bcolors.OKGREEN + "VALID" + bcolors.ENDC)
    except InvalidSignatureException:
        print("Signature validation: " + bcolors.FAIL + "NOT VALID" + bcolors.ENDC)

def _print_certificate(x509cert):
    print ("\nX509 CERTIFICATE: \n")
    print_x509cert(x509cert)

def _print_priv_key(priv_key, input_password):
    print("\nRSA PRIVATE KEY: \n")
    print_rsa_priv_key(priv_key, input_password)
    
def _print_pub_key(pub_key):
    print("\nRSA PUB KEY: \n")
    print_rsa_pub_key(pub_key)

def _print_signature(signature):
    print("Signature: \n" + signature.hex())


""""""""""""
""" MAIN """
""""""""""""
if __name__ == '__main__':
    #basic_demo()
    #test_eidas_link_did("./tests/data/tmp/rsakey.pem", b"passphrase", "./tests/data/tmp/x509cert.pem", "did:sov:55GkHamhTU1ZbTbV2ab9DE")
    #test_suite_crypto_hash()
    crypto_suite_test(
        [False, True, True, True], 
        "./tests/data/tmp/", 
        "./tests/data/tmp/rsakey.pem", 
        b"passphrase", 
        "./tests/data/tmp/x509cert.pem", 
        "did:sov:55GkHamhTU1ZbTbV2ab9DE",
        proofs,
        True
    )
    #test_generate_x509cert_and_key_and_store_to_disk("./tests/data/tmp/", b"passphrase")
    #test_sign_and_verify("./tests/data/tmp/rsakey.pem", b"passphrase", "did:sov:55GkHamhTU1ZbTbV2ab9DE")