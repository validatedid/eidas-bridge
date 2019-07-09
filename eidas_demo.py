from eidas_bridge.eidas_bridge import eidas_link_did, \
    eidas_get_service_endpoint_struct, eidas_sign_credential, eidas_verify_credential
from utils.crypto import eidas_hash_byte, eidas_hash_str, eidas_hash_hex,  \
    create_selfsigned_x509_certificate, store_rsa_key_and_x509cert_to_disk, \
    get_public_key_from_rsakey_str, x509_get_certificate_from_obj_str, \
    print_rsa_key, print_x509cert

_rsa_private_key_pem = "\
    -----BEGIN RSA PRIVATE KEY-----\
    Proc-Type: 4,ENCRYPTED\
    DEK-Info: AES-256-CBC,215EB960CA329313B8E88CCA74D5A7D2\
    \
    t7oMh75UwTVjhTM4v7i95wnzdElxBqCwG7F0xNO1SLwGAgqxmsoy4s8/blAxDzjq\
    ndguogUYB4bLFmQPQSnn3rJnySJ5LeHiS7eZoixHsf39/HhpMkFF/zW63ZiX8+J+\
    Mt3dpKmCczvyAAVd9ED1O61/k+ChU74wsJvr3Q+fnt8ZMqyme93bCQXMIIjsejCF\
    bEuzFTUReRn6sxQIv01yt8lZ4ztk4cyGFFCqnpfLX5NqWUfyf7oE4PiJ5PpI4AgO\
    HZdG+KzUl4K6dRlf7Yaaf4rC8WQy+RUy5Y57M9fmDyseaia9D/YtxEIKyxAJ2sB7\
    bxvNoJ5L3Y3zGZ+i8YUF/cvUPY3p7MjVfqISceYa06Rb3GDtU9968Dvo/arfDYEe\
    AsnQ9ZcT+XLmdwNtyX1MVf10+qWi0su7URF016z3v/KItjYX9Zp+a90rS9wCawYc\
    y+8hsezh0gO9afvJ/VehCd2wAq2cU7MaSwc9TTKhU5JqpbQh1Uj74erWFGx0TeN3\
    2OaxpS7P5aZN4FH6dzdGaSbAHVRKwbCuxk5A5ngqQe+jafl0J1Q2I79lQ6r9x0it\
    BJuZSVfi26UFSnHnp8OocQ+v1PoOcwQU3LNqlVOTc6vfGx1ZbrRsauYgI1S2vMCL\
    mlvCgGo3Y3SgeWpcVz7n51AsG093DjA1IaIaG+xkxIHUzdN2pXuiyP7KM43TFKra\
    U/o7jUZg7ewwPb0jfPZSaubIW4SUckawHg75NaJ3MISvkFBDs8FaQ/xj0H/NGaON\
    Twj43mmjadgEM28SFiRIxHeIteI6xzQWCUkzQukZK0kSMffB43dVdNttCrT6sHH3\
    ISk2xoLecA55fXVFLDlfvSyt6UyL4t126qecD//jfsT8JR85mQeLc8IPfEWpKp5s\
    N/tGGfwEdvosd4a6pt1mCQOam5v5GNA3nGcI4TCxHj1kcTiNL3WaCDTe/mO78bRs\
    1JrjUD4G5y1LDDTOrBpKcwNdGeRapY38Om7p7Le74eD3coU6RN+eugdFzMzWD1tL\
    c0yinoyGHgTzhsHl+etMQcSF9zfneDsUFuBafMXDoN0vV/XJJ6vWXYcuBkbxSNA7\
    J1jBTYEKp5C+iPeO69C+wi4m91u3MP2FitHzztF8IkzbDc54VTmnzqQyJ4PGC+P/\
    JubKs6WwlVZnHgjajMylg9d3p9qvoadoP+YsA3ARpAZHmtdyw8e9zGE5rdshZ5jI\
    DkRiEV5GuQt3ZQoBrNagIL9KU+QkZlJcH2nwV+hUgjgEm8sfdtmqQyqOUK+TPBMr\
    Nn7i+Yg3OciHT0R2glvbGAsdlWOLzORyt/qd0tyoIINlJYqaWRHFV9xRy5wlcKxk\
    UBFPbP/a2m40kZIcO/x9Cdz+jw+A5X2ZRKrSQuH05f/x7RHc7dg15WIVQz0hCz6t\
    XyrWiLg0QR3DB2oP2rE47AX1tSHn3JDOBKFT/lIgYrjV/7nQ+/HPSGro81ZwWp/V\
    0+5ZPi3qIww0zO5ZMdnxyConFsZ7WA5ojuDkI/p/akk8dujsOPqAhZYp6SLd8lo9\
    6ELjpHoPf7DE8qeUJO6gAcvv36BC6cQ54YqtnHS+RM1vuxG5mCtFFJlB5Ae2e5Cq\
    -----END RSA PRIVATE KEY-----\
"

_x509_cert_pem = "\
    -----BEGIN CERTIFICATE-----\
    MIIDYDCCAkigAwIBAgIUTrNlBhZkmfzpgGpVHWXsq6f8G38wDQYJKoZIhvcNAQEL\
    BQAwXTELMAkGA1UEBhMCRVMxEzARBgNVBAgMClRFU1RfU1RBVEUxEjAQBgNVBAcM\
    CVRFU1RfQ0lUWTEQMA4GA1UECgwHQ0FfQUNNRTETMBEGA1UEAwwKbXlzaXRlLmNv\
    bTAeFw0xOTA3MDkxMzQxNTVaFw0yMDA3MDgxMzQxNTVaMF0xCzAJBgNVBAYTAkVT\
    MRMwEQYDVQQIDApURVNUX1NUQVRFMRIwEAYDVQQHDAlURVNUX0NJVFkxEDAOBgNV\
    BAoMB0NBX0FDTUUxEzARBgNVBAMMCm15c2l0ZS5jb20wggEiMA0GCSqGSIb3DQEB\
    AQUAA4IBDwAwggEKAoIBAQC6CL2KDR3pNz5dRgnVXv1mqWRl2uISwSJ9R8UfR5l9\
    uLI79a1llrcjKfrm98EOttpg8Wp05AXALgLV2qPh0BwV5mu1Q93XrHxtmb13GBl/\
    du7HnTD9F1XlhEnuSYcPBMcOwmO0h9SoKVQq2Wfo7U0p2lV5hj2N7O/rvwpEA5UN\
    M68VCMKU8CHlMuHJQna7WBdBzzyrOZpfc9MJ0e54XT9sYUXQJbDWe639mxViJw7o\
    ntKiGMUk+7taxN+ByA5bKPF7YVim22r3VjnCSd4d/SfzxI8Vc+/QbkBGQNq/DoZa\
    3LXT1wy2iuuzVPM0KxNwHw9RZU+2BgonC/9rLX9Zri9TAgMBAAGjGDAWMBQGA1Ud\
    EQQNMAuCCWxvY2FsaG9zdDANBgkqhkiG9w0BAQsFAAOCAQEAPHlEmM+27TowcDaF\
    87vr5wbpB3f/sciiMmSGKODe1kN0zRVVdJ8TkqMvpdAlwc16pEI3GDVHNiU4KHOH\
    YagO2t+6I9ZvdIr4tI/QRDVHT1XqhWEVqyG6/jrRHMBaSuXeqg52X3EI7JH/tGYA\
    Ol/p78wJ0yIRbr7YfsPhR0PCwFdjY6ZcN/EB3PeZXQHK5RucunhiFISV8KEl5ELY\
    0oqNYpyHZX6VByMIuIpmynHnK4YikxJ2FbAncG3eo2wMbHGMMCcnpGjeXXRRbgP8\
    brJN2B7xks4rEaCAwF6b3lEKLfCspjaefUF1eKBK7HW7WBHCH8Z1A8zGFS1MeGIq\
    1VVEAw==\
    -----END CERTIFICATE-----\
"

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

""" RSA CRYPTO TEST SUITE """
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


if __name__ == '__main__':
    #basic_demo()
    #test_suite_hash()
    test_generate_x509cert_and_key_and_store_to_disk("./tests/data/tmp/")