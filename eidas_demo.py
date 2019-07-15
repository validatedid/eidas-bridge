# eidas_demo.py
""" EIDAS LIBRARY DEMO TO TEST ALL API FUNCTIONS """

import time
from eidas_bridge.eidas_bridge import eidas_link_did, \
    eidas_get_service_endpoint, eidas_sign_credential, eidas_verify_credential, \
    EIDASNotSupportedException
from eidas_bridge.utils.crypto import InvalidSignatureException, x509_load_certificate_from_data_bytes, \
    PKCS1v15_PADDING, PSS_PADDING, rsa_verify
from tests.data.common_data import eidas_link_inputs, service_endpoints, credentials, paddings
from tests.util import bcolors, print_object
from tests.crypto import create_selfsigned_x509_certificate, store_rsa_key_and_x509cert_to_disk, \
    print_rsa_pub_key, print_x509cert, eidas_crypto_hash_byte, eidas_crypto_hash_str, \
    eidas_crypto_hash_hex, rsa_load_private_key_from_file, x509_load_certificate_from_file, \
    x509_get_PEM_certificate_from_obj, print_rsa_priv_key, rsa_sign, load_pkcs12_file

""""""""""""""""""""""""
""" EIDAS BRIDGE TESTS """
""""""""""""""""""""""""

def basic_demo():

    """ Initial Demo: very basic """
    print(bcolors.HEADER + "1.- calling eidas link did: " + bcolors.ENDC)
    for eidas_link_input in eidas_link_inputs:
        print(bcolors.OKBLUE + "\n\r--- EIDAS LINK DID JSON STRUCT ---\n\r" + bcolors.ENDC)
        print (eidas_link_did(eidas_link_input[3], eidas_link_input[0], bytes.fromhex(eidas_link_input[1]), eidas_link_input[2]))

    print(bcolors.HEADER + "\n2.- calling eidas get service endpoint struct " + bcolors.ENDC)
    for service_endpoint in service_endpoints:
        print(bcolors.OKBLUE + "\n\r--- EIDAS SERVICE ENDPOINT JSON STRUCT ---\n\r" + bcolors.ENDC)
        print (eidas_get_service_endpoint(service_endpoint[0], service_endpoint[1]))

    print(bcolors.HEADER + "\n3.- calling eidas sign credential " + bcolors.ENDC)
    try:
        print (eidas_sign_credential(credentials[0]))
    except EIDASNotSupportedException:
        print(bcolors.WARNING + "\n\r--- EIDAS Library function NOT supported yet. ---\n\r" + bcolors.ENDC)

    print(bcolors.HEADER + "\n4.- calling eidas verify credential " + bcolors.ENDC)
    print (eidas_verify_credential(credentials[0]))

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

def test_crypto_hash_suite():
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

def test_sign_and_verify_from_key_file(path_to_key_file, input_password, message, padding, bprint):
    #load key
    rsa_priv_key = _load_key_from_file(path_to_key_file, input_password, bprint)

    #rsa signature
    signature = _sign(message, rsa_priv_key, padding, bprint)

    #rsa validation with the public key
    _verify(signature, message, rsa_priv_key.public_key(), padding, bprint)

def test_sign_from_file_verify_from_cert_file(path_to_key_file, input_password, 
    path_to_cert_file, message, padding, bprint):
    #load key
    rsa_priv_key = _load_key_from_file(path_to_key_file, input_password, bprint)
    #load certificate
    x509cert = _load_cert_from_file(path_to_cert_file, bprint)

    #rsa signature
    signature = _sign(message, rsa_priv_key, padding, bprint)
    
    #rsa validation with the public key from the loaded certificate
    _verify(signature, message, x509cert.public_key(), padding, bprint)

def verify_signature_from_cert_file(path_to_cert_file, message, signature, padding, bprint):
    #load certificate
    x509cert = _load_cert_from_file(path_to_cert_file, bprint)

    #rsa validation with the public key from the loaded certificate
    _verify(bytes.fromhex(signature), message, x509cert.public_key(), padding, bprint)

def verify_signature_from_cert_pem_data(pem_cert_data, message, signature, padding, bprint):
    #load certificate 
    x509cert = _load_cert_from_pem(pem_cert_data, bprint)

    #rsa validation with the public key from the loaded certificate
    _verify(bytes.fromhex(signature), message, x509cert.public_key(), padding, bprint)

def test_sign_and_verify_from_p12file_using_key(path_to_p12_file, p12_password, message, padding, bprint):
    # Load key and cert from p12 file
    rsa_priv_key, *_ = _load_key_and_cert_from_p12file(path_to_p12_file, p12_password, bprint)

    #rsa signature
    signature = _sign(message, rsa_priv_key, padding, bprint)

    #rsa validation with the public key from private key
    _verify(signature, message, rsa_priv_key.public_key(), padding, bprint)

def test_sign_and_verify_fron_p12file_using_cert(path_to_p12_file, p12_password, message, padding, bprint):
    # Load key and cert from p12 file
    rsa_priv_key, x509cert = _load_key_and_cert_from_p12file(path_to_p12_file, p12_password, bprint)

    #rsa signature
    signature = _sign(message, rsa_priv_key, padding, bprint)

    #rsa validation with the public key from certificate
    _verify(signature, message, x509cert.public_key(), padding, bprint)


""" CRYPTO SUITE """

def _crypto_suite_test(tests_to_execute, path_to_dir_to_store, path_to_key_file, input_password, 
    path_to_cert_file, path_to_p12_file, p12_password, message, x509cert, proof, proof_padding, new_padding, 
    bprint):
    if tests_to_execute[0]:
        print("\nCRYPTO TEST 1: Generate x509 certificate and RSA Key and store to disk:\n")
        input("Press Enter to continue...")
        test_generate_x509cert_and_key_and_store_to_disk(path_to_dir_to_store, 
        input_password, bprint)
    if tests_to_execute[1]:
        print("\nCRYPTO TEST 2: Sign a message with %s padding type, with a RSA Key loaded from file and \
Verify the signature with the correspondent public key:\n" % new_padding)
        input("Press Enter to continue...")
        test_sign_and_verify_from_key_file(path_to_key_file, input_password, message, new_padding, bprint)
    if tests_to_execute[2]:
        print("\nCRYPTO TEST 3: Sign a message with %s padding type, with a RSA Key loaded from file and \
Verify the signature with the certificate public key loaded from a file:\n" % new_padding)
        input("Press Enter to continue...")
        test_sign_from_file_verify_from_cert_file(path_to_key_file, input_password, 
        path_to_cert_file, message, new_padding, bprint)
    if tests_to_execute[3]:
        print("\nCRYPTO TEST 4: Verifies signature with %s padding type and getting \
the public key from a certificate stored in disk:\n" % proof_padding)
        input("Press Enter to continue...")
        verify_signature_from_cert_file(path_to_cert_file, message, proof, proof_padding, bprint)
    if tests_to_execute[4]:
        print("\nCRYPTO TEST 5: Verifies signatures with %s padding type and getting \
the public key from a certificate stored in a list:\n" % proof_padding)
        input("Press Enter to continue...")
        verify_signature_from_cert_pem_data(x509cert, message, proof, proof_padding, bprint)
    if tests_to_execute[5]:
        print("\nSIGN & VERIFY TEST 6: Using a PKCS#12 file and using the public key \
from the private key to verify:\n")
        input("Press Enter to continue...")
        test_sign_and_verify_from_p12file_using_key(path_to_p12_file, p12_password, message, new_padding, bprint)
    if tests_to_execute[6]:
        print("\nSIGN & VERIFY TEST 7: Using a PKCS#12 file and using the public key \
from the certificate to verify:\n")
        input("Press Enter to continue...")
        test_sign_and_verify_fron_p12file_using_cert(path_to_p12_file, p12_password, message, new_padding, bprint)

""""""""""""""""""""""""
""" AUX FUNCTIONS    """
""""""""""""""""""""""""

def _load_key_and_cert_from_p12file(path_to_p12_file, p12_password, bprint) -> (bytes, bytes):
    #load key and certificate(s)
    rsa_priv_key, x509cert, *_ = load_pkcs12_file(path_to_p12_file, p12_password)

    if bprint:
        _print_certificate(x509cert)
        _print_priv_key(rsa_priv_key, p12_password)
        _print_pub_key(rsa_priv_key.public_key())
    
    return rsa_priv_key, x509cert

def _load_cert_from_pem(pem_cert_data, bprint) -> bytes:
    #load certificate and convert it to a PEM byte data
    x509cert = x509_load_certificate_from_data_bytes(pem_cert_data)

    if bprint:
        _print_certificate(x509cert)
        _print_pub_key(x509cert.public_key())
    
    return x509cert

def _load_cert_from_file(path_to_cert_file, bprint) -> bytes:
    #load certificate and convert it to a PEM byte data
    x509cert = x509_load_certificate_from_file(path_to_cert_file)
   
    if bprint:
        _print_certificate(x509cert)
        _print_pub_key(x509cert.public_key())

    return x509cert

def _load_key_from_file(path_to_key_file, input_password, bprint) -> bytes:
    #load key
    rsa_priv_key = rsa_load_private_key_from_file(path_to_key_file, input_password)
    
    if bprint:
        _print_priv_key(rsa_priv_key, input_password)
        _print_pub_key(rsa_priv_key.public_key())
    
    return rsa_priv_key

def _sign(message, rsa_priv_key, padding, bprint) -> bytes:
    signature = rsa_sign(message.encode('utf-8'), rsa_priv_key, padding)
    if bprint:
        _print_signature(signature)

    return signature

def _verify(signature, message, pub_key, padding, bprint):
    #rsa validation with the public key from the loaded certificate
    if bprint:
        _print_signature(signature)
    try:
        rsa_verify(signature, message.encode('utf-8'), pub_key, padding)
        print("\nSignature validation: " + bcolors.OKGREEN + "VALID\n" + bcolors.ENDC)
    except InvalidSignatureException:
        print("\nSignature validation: " + bcolors.FAIL + "NOT VALID\n" + bcolors.ENDC)

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

def test_crypto_suite_loop(tests_to_execute, path_to_dir_to_store, path_to_key_file, input_password, 
    path_to_cert_file, path_to_p12_file, p12_password, eidas_link_inputs, paddings, bprint):
    for eidas_link_input in eidas_link_inputs:
        for padding in paddings:
            _crypto_suite_test(
                tests_to_execute, 
                path_to_dir_to_store, 
                path_to_key_file, 
                input_password, 
                path_to_cert_file, 
                path_to_p12_file,
                p12_password, 
                eidas_link_input[3], # dids
                eidas_link_input[0], # certificates
                eidas_link_input[1], # proof
                eidas_link_input[2], # proof padding 
                padding, # padding type on new signatures
                bprint
            )

""""""""""""
""" MAIN """
""""""""""""
if __name__ == '__main__':
    start_time = time.time()
    print(bcolors.BOLD + "\n--- INIT EIDAS MAIN DEMO TEST SUITE ---\n\r" + bcolors.ENDC)
    
    print(bcolors.HEADER + "\n--- INIT BASIC DEMO TEST SUITE ---\n\r" + bcolors.ENDC)
    input("Press Enter to continue...")
    basic_demo()

    """
    print(bcolors.HEADER + "\n--- INIT CRYPTO HASH TEST SUITE ---\n\r" + bcolors.ENDC)
    input("Press Enter to continue...")
    test_crypto_hash_suite()

    print(bcolors.HEADER + "\n--- INIT CRYPTO TEST SUITE ---\n\r" + bcolors.ENDC)
    input("Press Enter to continue...")
    test_crypto_suite_loop(
        [False, False, False, False, True, False, False], 
        "./tests/data/tmp/", 
        "./tests/data/rsakey.pem", 
        b"passphrase", 
        "./tests/data/x509cert.pem", 
        "./tests/data/certificate.p12",
        b"passphrase", 
        eidas_link_inputs,
        paddings,
        True
    )
    """
    elapsed_time = time.time() - start_time
    print(bcolors.BOLD + "\n--- END EIDAS MAIN DEMO TEST SUITE ---\n\r" + bcolors.ENDC)
    print("--- Total time: " + bcolors.OKGREEN + str(round(elapsed_time, 2)) + " seconds " + \
        bcolors.ENDC + "---\n\r")