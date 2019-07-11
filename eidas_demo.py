# eidas_demo.py
""" EIDAS LIBRARY DEMO TO TEST ALL API FUNCTIONS """

from eidas_bridge.eidas_bridge import eidas_link_did, \
    eidas_get_service_endpoint_struct, eidas_sign_credential, eidas_verify_credential
from eidas_bridge.utils.crypto import InvalidSignatureException, x509_load_certificate_from_data_bytes, \
    PKCS1v15_PADDING, PSS_PADDING, rsa_verify
from tests.data.common_data import dids, x509certs, proofs, endpoints, credentials
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
    path_to_cert_file, did, bprint, padding):
    #load key
    rsa_priv_key = rsa_load_private_key_from_file(path_to_key_file, input_password)

    #rsa signature
    proof = rsa_sign(did.encode('utf-8'), rsa_priv_key, padding)
    if bprint:
        _print_signature(proof)

    #load certificate and convert it to a PEM byte data
    x509cert = x509_load_certificate_from_file(path_to_cert_file)
    pem_cert_data = x509_get_PEM_certificate_from_obj(x509cert)

    #create an eIDAS Link DID structure and print to stdout
    print(eidas_link_did(did, pem_cert_data, proof, padding))

def test_eidas_link_did_all_paddings(path_to_key_file, input_password, 
    path_to_cert_file, did, bprint, bpadding):
    if bpadding:
        test_eidas_link_did(path_to_key_file, input_password, path_to_cert_file, did, bprint, PKCS1v15_PADDING)
        test_eidas_link_did(path_to_key_file, input_password, path_to_cert_file, did, bprint, PSS_PADDING)
    else:
        test_eidas_link_did(path_to_key_file, input_password, path_to_cert_file, did, bprint, PSS_PADDING)


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

def test_sign_and_verify_from_key_file(path_to_key_file, input_password, message, bprint, padding):
    #load key
    rsa_priv_key = _load_key_from_file(path_to_key_file, input_password, bprint)

    #rsa signature
    signature = _sign(message, rsa_priv_key, padding, bprint)

    #rsa validation with the public key
    _verify(signature, message, rsa_priv_key.public_key(), padding)

def test_sign_from_file_verify_from_cert_file(path_to_key_file, input_password, 
    path_to_cert_file, message, bprint, padding):
    #load key
    rsa_priv_key = _load_key_from_file(path_to_key_file, input_password, bprint)
    #load certificate
    x509cert = _load_cert_from_file(path_to_cert_file, bprint)

    #rsa signature
    signature = _sign(message, rsa_priv_key, padding, bprint)
    
    #rsa validation with the public key from the loaded certificate
    _verify(signature, message, x509cert.public_key(), padding)

def verify_signature_from_cert_file(path_to_cert_file, message, signature, bprint, padding):
    #load certificate
    x509cert = _load_cert_from_file(path_to_cert_file, bprint)

    #rsa validation with the public key from the loaded certificate
    _verify(signature, message, x509cert.public_key(), padding)

def test_verify_signature_from_cert_file_loop(path_to_cert_file, message, proofs, bprint,\
    padding):
    for signature in proofs:
        verify_signature_from_cert_file(path_to_cert_file, message, bytes.fromhex(signature), \
            bprint, padding)

def verify_signature_from_cert_pem_data(pem_cert_data, message, signature, bprint, padding):
    #load certificate 
    x509cert = _load_cert_from_pem(pem_cert_data, bprint)

    #rsa validation with the public key from the loaded certificate
    _verify(signature, message, x509cert.public_key(), padding)

def test_verify_signature_from_cert_pem_data_loop(x509certs, message, proofs, bprint, padding):
    i = 0
    for certificate in x509certs:
        print("Using the [" + str(i) + "] certificate")
        j = 0
        for signature in proofs:
            print("Using the [" + str(j) + "] signature")
            verify_signature_from_cert_pem_data(certificate, message, bytes.fromhex(signature), 
            bprint, padding)
            j += 1
        i += 1

def test_sign_and_verify_from_p12file_using_key(path_to_p12_file, p12_password, message, bprint, padding):
    # Load key and cert from p12 file
    rsa_priv_key, *_ = _load_key_and_cert_from_p12file(path_to_p12_file, p12_password, bprint)

    #rsa signature
    signature = _sign(message, rsa_priv_key, padding, bprint)

    #rsa validation with the public key from private key
    _verify(signature, message, rsa_priv_key.public_key(), padding)

def test_sign_and_verify_fron_p12file_using_cert(path_to_p12_file, p12_password, message, bprint, padding):
    # Load key and cert from p12 file
    rsa_priv_key, x509cert = _load_key_and_cert_from_p12file(path_to_p12_file, p12_password, bprint)

    #rsa signature
    signature = _sign(message, rsa_priv_key, padding, bprint)

    #rsa validation with the public key from certificate
    _verify(signature, message, x509cert.public_key(), padding)


""" CRYPTO SUITE """

def crypto_suite_test(tests_to_execute, path_to_dir_to_store, path_to_key_file, input_password, 
    path_to_cert_file, path_to_p12_file, p12_password, message, proofs, x509certs, bprint, bpadding):
    if bpadding:
        crypto_suite_test_padding_set(tests_to_execute, path_to_dir_to_store, path_to_key_file, input_password, 
        path_to_cert_file, path_to_p12_file, p12_password, message, proofs, x509certs, bprint, PKCS1v15_PADDING)
        crypto_suite_test_padding_set(tests_to_execute, path_to_dir_to_store, path_to_key_file, input_password, 
        path_to_cert_file, path_to_p12_file, p12_password, message, proofs, x509certs, bprint, PSS_PADDING)
    else:
        crypto_suite_test_padding_set(tests_to_execute, path_to_dir_to_store, path_to_key_file, input_password, 
        path_to_cert_file, path_to_p12_file, p12_password, message, proofs, x509certs, bprint, PSS_PADDING)

def crypto_suite_test_padding_set(tests_to_execute, path_to_dir_to_store, path_to_key_file, input_password, 
    path_to_cert_file, path_to_p12_file, p12_password, message, proofs, x509certs, bprint, padding):
    if tests_to_execute[0]:
        print("CRYPTO TEST 1: Generate x509 certificate and RSA Key and store to disk:\n")
        test_generate_x509cert_and_key_and_store_to_disk(path_to_dir_to_store, 
        input_password, bprint)
    if tests_to_execute[1]:
        print("\nCRYPTO TEST 2: Sign a message with a RSA Key loaded from file and \
Verify the signature with the correspondent public key:\n")
        test_sign_and_verify_from_key_file(path_to_key_file, input_password, message, bprint, padding)
    if tests_to_execute[2]:
        print("\nCRYPTO TEST 3: Sign a message with a RSA Key loaded from file and \
Verify the signature with the certificate public key loaded from a file:\n")
        test_sign_from_file_verify_from_cert_file(path_to_key_file, input_password, 
        path_to_cert_file, message, bprint, padding)
    if tests_to_execute[3]:
        print("\nCRYPTO TEST 4: Verifies signatures passed as a list and getting \
the public key from a certificate stored in disk:\n")
        test_verify_signature_from_cert_file_loop(path_to_cert_file, message, proofs, 
        bprint, padding)
    if tests_to_execute[4]:
        print("\nCRYPTO TEST 5: Verifies signatures passed as a list and getting \
the public key from a certificate stored in a list:\n")
        test_verify_signature_from_cert_pem_data_loop(x509certs, message, proofs, 
        bprint, padding)
    if tests_to_execute[5]:
        print("SIGN & VERIFY TEST 6: Using a PKCS#12 file and using the public key \
from the private key to verify:\n")
        test_sign_and_verify_from_p12file_using_key(path_to_p12_file, p12_password, message, bprint, padding)
    if tests_to_execute[6]:
        print("SIGN & VERIFY TEST 7: Using a PKCS#12 file and using the public key \
from the certificate to verify:\n")
        test_sign_and_verify_fron_p12file_using_cert(path_to_p12_file, p12_password, message, bprint, padding)



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

def _verify(signature, message, pub_key, padding):
    #rsa validation with the public key from the loaded certificate
    try:
        rsa_verify(signature, message.encode('utf-8'), pub_key, padding)
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
    """
    test_eidas_link_did_all_paddings(
        "./tests/data/tmp/rsakey.pem", 
        b"passphrase", 
        "./tests/data/tmp/x509cert.pem", 
        "did:sov:55GkHamhTU1ZbTbV2ab9DE", 
        False, 
        True)
    """
    #test_suite_crypto_hash()
    
    crypto_suite_test(
        [False, True, True, True, True, True, True], 
        "./tests/data/tmp/", 
        "./tests/data/rsakey.pem", 
        b"passphrase", 
        "./tests/data/x509cert.pem", 
        "./tests/data/certificate.p12",
        b"passphrase", 
        "did:sov:55GkHamhTU1ZbTbV2ab9DE",
        proofs,
        x509certs,
        False,
        True
    )