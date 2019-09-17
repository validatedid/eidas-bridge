# common_data.py
""" Data to used alongside the test suite """

from eidas_bridge.utils.crypto import PKCS1v15_PADDING, PSS_PADDING

dids = [
    "did:sov:55GkHamhTU1ZbTbV2ab9DE"
]

eidas_inputs = [
    (
        '-----BEGIN CERTIFICATE-----\nMIIB0TCCAXegAwIBAgIUchXErFvhmOK5ri9v7FHWWWQSINUwCgYIKoZIzj0EAwIw\nXTELMAkGA1UEBhMCRVMxEzARBgNVBAgMClRFU1RfU1RBVEUxEjAQBgNVBAcMCVRF\nU1RfQ0lUWTEQMA4GA1UECgwHQ0FfQUNNRTETMBEGA1UEAwwKbXlzaXRlLmNvbTAe\nFw0xOTA5MTYxNTQ4MDBaFw0yMDA5MTUxNTQ4MDBaMF0xCzAJBgNVBAYTAkVTMRMw\nEQYDVQQIDApURVNUX1NUQVRFMRIwEAYDVQQHDAlURVNUX0NJVFkxEDAOBgNVBAoM\nB0NBX0FDTUUxEzARBgNVBAMMCm15c2l0ZS5jb20wVjAQBgcqhkjOPQIBBgUrgQQA\nCgNCAATph0QsUOGPAaOzh+DDKwZ4QJFObDIQgMmU29yk4IUMvpDA7RMd4NEhKXiK\nqmT/dRDnbFM1jxJ6/+3A0fsrdXmloxgwFjAUBgNVHREEDTALgglsb2NhbGhvc3Qw\nCgYIKoZIzj0EAwIDSAAwRQIhALZ+suOUlPI5wNDKJQAtl59Yu4utWEkoyfBqKjSp\n2B3ZAiAgTx47NhtUjNSgEY9PybfMBR1yJCjHOMUDLCjqhdhG/w==\n-----END CERTIFICATE-----\n',
        '3046022100aacf8418bb30cffe32e053682968ca8a6a7ae198b1733676ed6ed0f352c6fcea022100970684b7e768e9b6a5b13e4aff77a38102c9ab2325e217f6ba0a9136e3d95d4d',
        PSS_PADDING,
        "did:sov:55GkHamhTU1ZbTbV2ab9DE" 
    )
]
"""
eidas_inputs = [
    (
        '-----BEGIN CERTIFICATE-----\nMIIDYDCCAkigAwIBAgIUI63ffVceaNc1kN9O0q/4jSjbkU0wDQYJKoZIhvcNAQEL\nBQAwXTELMAkGA1UEBhMCRVMxEzARBgNVBAgMClRFU1RfU1RBVEUxEjAQBgNVBAcM\nCVRFU1RfQ0lUWTEQMA4GA1UECgwHQ0FfQUNNRTETMBEGA1UEAwwKbXlzaXRlLmNv\nbTAeFw0xOTA3MDkxNDA3MjBaFw0yMDA3MDgxNDA3MjBaMF0xCzAJBgNVBAYTAkVT\nMRMwEQYDVQQIDApURVNUX1NUQVRFMRIwEAYDVQQHDAlURVNUX0NJVFkxEDAOBgNV\nBAoMB0NBX0FDTUUxEzARBgNVBAMMCm15c2l0ZS5jb20wggEiMA0GCSqGSIb3DQEB\nAQUAA4IBDwAwggEKAoIBAQDm6RhyIeFZHn4bGQ/2UQ+aflczCo3Ej04LJXfiIU1Q\nt7xRq3e+uh7nTLffnS7fj/ZZBBREmR/D/SJBTlxv7WQEbscV/pf2LoZLjoC4M4ye\n43lUHRmWsm4J50tu9zcSheqXCRyAK/Ai6RUBy86NKXMFTUp/ONxS0BxJg8GU03Xd\nXGnYzdmZZXGDnublGYq03gD/cZYguS7/HS8v/MckdmjYPTy2syGL9unYkjWn7vig\niaDc2leAM4agKB6PODJSFla15HLoqskKX1SgtLJUHxu/FOo6hYdCt+GxpV1xhl/r\nEf3/SFeTZrJgL11m5ABDli2zAmCn4bjBNnNcXWy5QV0pAgMBAAGjGDAWMBQGA1Ud\nEQQNMAuCCWxvY2FsaG9zdDANBgkqhkiG9w0BAQsFAAOCAQEAYPUn0TzGyn438++1\nV2jMHC653C8tn3vVF5nTT7Td+ihc+KaaNDYsgyY2JpBIMRwlNgoNU0Da3P/9ZDn3\nlFJElUg8WpWPvpXtbS4udqn6UcfT9mFJtkzKg3CK5i50GRCabV9FPbY1bzYtUbY+\nEntXtI2h0dxcgzgOw6pkXFB3O7ZbbshpqWTlHtTtbxxrOFq0zcpyS92G+NTF6ASS\nhXcIf90du/mBWd2dinF/w2nkRAWfGBy8bGnUSJ93rPVwLjI0PDeHh7+PSQ+3X6mG\n5DI9EmzEC7esW6wJbhgiOYXLavAOmLfI0yq/z8SZMvFYwBE69VuGfPSj/u4nIhA5\nK0Qgnw==\n-----END CERTIFICATE-----\n',
        '4f1bb7069e1508901e83d9dd71043e35fbc8ecf3077625206dd00cf8f12365096cc1cf07822479e571689bc67c50a7d9ca66c43865e490044729af3356e853073073c11e9fa517f7b35748146c1c1101406f66866969ad5915054e3633ab3c247d6b09be909ece6d018ad309b1b34c45b223227d74928278640e0e6a62de0309309e609e8927eb7abd098dfb8a30e8c91fde3ea4fbe804b2967db2c994d303de1e6ac837cfd2a11414ace2bd75148e917b3505f17fabc4805484164a69fdc1d28122e977c1fa4f62b39a601915d8fe0b1bd6e2932db6c8ca3b2bca3ab04f3aebf83d081122d42248dc2a2f292f2c2bfc42244c3118109ab9f001a85cbdd52f71',
        PSS_PADDING,
        "did:sov:55GkHamhTU1ZbTbV2ab9DE"
    ),
    (
        '-----BEGIN CERTIFICATE-----\nMIIDYDCCAkigAwIBAgIUI63ffVceaNc1kN9O0q/4jSjbkU0wDQYJKoZIhvcNAQEL\nBQAwXTELMAkGA1UEBhMCRVMxEzARBgNVBAgMClRFU1RfU1RBVEUxEjAQBgNVBAcM\nCVRFU1RfQ0lUWTEQMA4GA1UECgwHQ0FfQUNNRTETMBEGA1UEAwwKbXlzaXRlLmNv\nbTAeFw0xOTA3MDkxNDA3MjBaFw0yMDA3MDgxNDA3MjBaMF0xCzAJBgNVBAYTAkVT\nMRMwEQYDVQQIDApURVNUX1NUQVRFMRIwEAYDVQQHDAlURVNUX0NJVFkxEDAOBgNV\nBAoMB0NBX0FDTUUxEzARBgNVBAMMCm15c2l0ZS5jb20wggEiMA0GCSqGSIb3DQEB\nAQUAA4IBDwAwggEKAoIBAQDm6RhyIeFZHn4bGQ/2UQ+aflczCo3Ej04LJXfiIU1Q\nt7xRq3e+uh7nTLffnS7fj/ZZBBREmR/D/SJBTlxv7WQEbscV/pf2LoZLjoC4M4ye\n43lUHRmWsm4J50tu9zcSheqXCRyAK/Ai6RUBy86NKXMFTUp/ONxS0BxJg8GU03Xd\nXGnYzdmZZXGDnublGYq03gD/cZYguS7/HS8v/MckdmjYPTy2syGL9unYkjWn7vig\niaDc2leAM4agKB6PODJSFla15HLoqskKX1SgtLJUHxu/FOo6hYdCt+GxpV1xhl/r\nEf3/SFeTZrJgL11m5ABDli2zAmCn4bjBNnNcXWy5QV0pAgMBAAGjGDAWMBQGA1Ud\nEQQNMAuCCWxvY2FsaG9zdDANBgkqhkiG9w0BAQsFAAOCAQEAYPUn0TzGyn438++1\nV2jMHC653C8tn3vVF5nTT7Td+ihc+KaaNDYsgyY2JpBIMRwlNgoNU0Da3P/9ZDn3\nlFJElUg8WpWPvpXtbS4udqn6UcfT9mFJtkzKg3CK5i50GRCabV9FPbY1bzYtUbY+\nEntXtI2h0dxcgzgOw6pkXFB3O7ZbbshpqWTlHtTtbxxrOFq0zcpyS92G+NTF6ASS\nhXcIf90du/mBWd2dinF/w2nkRAWfGBy8bGnUSJ93rPVwLjI0PDeHh7+PSQ+3X6mG\n5DI9EmzEC7esW6wJbhgiOYXLavAOmLfI0yq/z8SZMvFYwBE69VuGfPSj/u4nIhA5\nK0Qgnw==\n-----END CERTIFICATE-----\n',
        'b0c86e06345f1b1b8b50696b5b42458699359e7dde13f535d7598db06891ccd7f4558f8262e23d8825cb65d0f16c72e53f93db7aa51b0831365db2dc8bbefc17d2c535646122ee1e448853044eeb83ffa944fac27e461ed41aa0f9d2079f49b60c88413fcedb287886094a831c79979b9323eac8fdabc1447facdd629d5533d6bc3f1a6a4ba4e420b7733b8617fe15f4f7a9ec81c0ae5b312dab6634082b29450bb77c19cda733719ecc8d758ec7988e39ff1f23dc5cf023156a82f1a73aaf2860d19dc64b452b4b15aa651d8845dbef97f07e3021babd5bdab3b353de271f0c3f95c29087f332d912a684560cad91e097a8978f42e8587b6c034e58ebbe1175',
        PKCS1v15_PADDING,
        "did:sov:55GkHamhTU1ZbTbV2ab9DE"
    )
]"""

paddings = [
    #PSS_PADDING,
    PKCS1v15_PADDING
]

all_type_dids = [
    b"\xd6\x98\x04\x88\xd2-\xc1D\x02\x15\xc9Z\x9bK \x8f\xe0\x8b5\xd0Z$",
    "did:sov:55GkHamhTU1ZbTbV2ab9DE",
    0
]

all_type_certificates = [
    b"\xd6\x98\x04\x88\xd2-\xc1D\x02\x15\xc9Z\x9bK \x8f\xe0\x8b5\xd0Z$",
    0,
    ""
]

bad_type_proofs = [
    b"this is a proof",
    20
]

service_endpoints = [
    (
        "did:sov:55GkHamhTU1ZbTbV2ab9DE", 
        "http://service_endpoint.sample/did:sov:55GkHamhTU1ZbTbV2ab9DE/eidas"
    ),
    (
        "did:example:21tDAKCERh95uGgKbJNHYp",
        "http://service_endpoint.sample/did:example:21tDAKCERh95uGgKbJNHYp/eidas"
    )
]

bad_type_endpoints = [
    b"\xd6\x98\x04\x88\xd2-\xc1D\x02\x15\xc9Z\x9bK \x8f\xe0\x8b5\xd0Z$",
    0
]

credentials = [
    {
        "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "https://www.w3.org/2018/credentials/examples/v1"
        ],
        "id": "http://example.edu/credentials/3732",
        "type": ["VerifiableCredential", "UniversityDegreeCredential"],
        "issuer": "did:example:21tDAKCERh95uGgKbJNHYp",
        "issuanceDate": "2010-01-01T19:23:24Z",
        "credentialSubject": {
            "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
            "degree": {
                "type": "BachelorDegree",
                "name": "Bachelor of Science and Arts"
                }  
            },
        "proof": {
            "type": "RsaSignature2018",
            "created": "2018-06-18T21:19:10Z",
            "proofPurpose": "assertionMethod",
            "verificationMethod": "https://example.com/jdoe/keys/1",
            "jws": "eyJhbGciOiJQUzI1NiIsImI2NCI6ZmFsc2UsImNyaXQiOlsiYjY0Il19DJBMvvFAIC00nSGB6Tn0XKbbF9XrsaJZREWvR2aONYTQQxnyXirtXnlewJMBBn2h9hfcGZrvnC1b6PgWmukzFJ1IiH1dWgnDIS81BH-IxXnPkbuYDeySorc4QU9MJxdVkY5EL4HYbcIfwKj6X4LBQ2_ZHZIu1jdqLcRZqHcsDF5KKylKc1THn5VRWy5WhYg_gBnyWny8E6Qkrze53MR7OuAmmNJ1m1nN8SxDrG6a08L78J0-Fbas5OjAQz3c17GY8mVuDPOBIOVjMEghBlgl3nOi1ysxbRGhHLEK4s0KKbeRogZdgt1DkQxDFxxn41QWDw_mmMCjs9qxg0zcZzqEJw"
        }
    }
] 

bad_credentials = [
    {
        "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "https://www.w3.org/2018/credentials/examples/v1"
        ],
        "id": "http://example.edu/credentials/3732",
        "type": ["VerifiableCredential", "UniversityDegreeCredential"],
        "credentialSubject": {
            "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
            "degree": {
                "type": "BachelorDegree",
                "name": "Bachelor of Science and Arts"
                }  
            },
        "proof": {}
    }
] 

bad_type_credentials = [
    b"\xd6\x98\x04\x88\xd2-\xc1D\x02\x15\xc9Z\x9bK \x8f\xe0\x8b5\xd0Z$",
    0
] 

did_documents = [
    {
        "@context": "https://w3id.org/did/v1",
        "id": "did:example:21tDAKCERh95uGgKbJNHYp",
        "authentication": [{
            "id": "did:example:21tDAKCERh95uGgKbJNHYp#keys-1",
            "type": "RsaVerificationKey2018",
            "controller": "did:example:21tDAKCERh95uGgKbJNHYp",
            "publicKeyPem": "-----BEGIN PUBLIC KEY...END PUBLIC KEY-----\r\n"
        }],
        "service": [{
            "id": "did:example:21tDAKCERh95uGgKbJNHYp#vc",
            "type": "VerifiableCredentialService",
            "serviceEndpoint": "https://example.com/vc/"
        }, {
            "id": "did:example:21tDAKCERh95uGgKbJNHYp#eidas",
            "type": "EidasService",
            "serviceEndpoint": "http://localhost:8000/did:example:21tDAKCERh95uGgKbJNHYp/eidas"
        }]
    }
]

bad_did_documents = [
    {
        "@context": "https://w3id.org/did/v1",
        "authentication": [{
            "id": "did:example:123456789abcdefghi#keys-1",
            "type": "RsaVerificationKey2018",
            "controller": "did:example:123456789abcdefghi",
            "publicKeyPem": "-----BEGIN PUBLIC KEY...END PUBLIC KEY-----\r\n"
        }],
        "service": [{
            "id": "did:example:123456789abcdefghi#vc",
            "type": "VerifiableCredentialService",
            "serviceEndpoint": "https://example.com/vc/"
        }]
    },
    {
        "@context": "https://w3id.org/did/v1",
        "id": "did:example:123456789abcdefghi",
        "authentication": [{
            "id": "did:example:123456789abcdefghi#keys-1",
            "type": "RsaVerificationKey2018",
            "controller": "did:example:123456789abcdefghi",
            "publicKeyPem": "-----BEGIN PUBLIC KEY...END PUBLIC KEY-----\r\n"
        }],
        "service": [{
            "id": "did:example:123456789abcdefghi#vc",
            "type": "VerifiableCredentialService",
            "serviceEndpoint": "https://example.com/vc/"
        }]
    }
]

bad_obj_type_paddings = [
    b"\xd6\x98\x04\x88\xd2-\xc1D\x02\x15\xc9Z\x9bK \x8f\xe0\x8b5\xd0Z$",
    0
]

bad_type_paddings = [
    "new_padding"
]

crypto_testdata = [
    ("","e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"),
    (" ","36a9e7f1c95b82ffb99743e0c5c4ce95d83c9a430aac59f84ef3cbfab6145068"),
    ("a","ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb"),
    ("0","5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9"),
    ("did:sov:", "97b40a411bf0e69968c6a0280c88f0d4f170245522d2d07c0cc39ffeffeb7bb2"),
    ("55GkHamhTU1ZbTbV2ab9DE", "9f4fc75928e784dbe2e5a33500aaa08a11906b02ef38309bf23208dca4452ef8"),
    ("did:sov:55GkHamhTU1ZbTbV2ab9DE","32eaebf15929b44167130a124c73b4652f122b9fc92ef5bde91a32f70c2bf049"),
    ("did:test:abcdefghijkl","eff857db6f037dec456ab0802998313059731f39a3f45b72413af30610f79f8c")
]

eidas_services = [
    {
        "id": "did:sov:55GkHamhTU1ZbTbV2ab9DE#eidas",
        "type": "EidasService",
        "serviceEndpoint": "http://service_endpoint.sample/did:sov:55GkHamhTU1ZbTbV2ab9DE/eidas"
    },
    {
        "id": "did:example:21tDAKCERh95uGgKbJNHYp#eidas",
        "type": "EidasService",
        "serviceEndpoint": "http://service_endpoint.sample/did:example:21tDAKCERh95uGgKbJNHYp/eidas"
    }
]

did_doc_services = [
    {
        "id": "did:example:123456789abcdefghi#openid",
        "type": "OpenIdConnectVersion1.0Service",
        "serviceEndpoint": "https://openid.example.com/"
    }, 
    {
        "id": "did:example:123456789abcdefghi#vcr",
        "type": "CredentialRepositoryService",
        "serviceEndpoint": "https://repository.example.com/service/8377464"
    }, 
    {
        "id": "did:example:123456789abcdefghi#xdi",
        "type": "XdiService",
        "serviceEndpoint": "https://xdi.example.com/8377464"
    }, 
    {
        "id": "did:example:123456789abcdefghi#agent",
        "type": "AgentService",
        "serviceEndpoint": "https://agent.example.com/8377464"
    }, 
    {
        "id": "did:example:123456789abcdefghi#hub",
        "type": "HubService",
        "serviceEndpoint": "https://hub.example.com/.identity/did:example:0123456789abcdef/"
    }, 
    {
        "id": "did:example:123456789abcdefghi#messages",
        "type": "MessagingService",
        "serviceEndpoint": "https://example.com/messages/8377464"
    }, 
    {
        "id": "did:example:123456789abcdefghi#inbox",
        "type": "SocialWebInboxService",
        "serviceEndpoint": "https://social.example.com/83hfh37dj",
        "description": "My public social inbox",
            "spamCost": {
            "amount": "0.50",
            "currency": "USD"
        }
    }, 
    {
        "id": "did:example:123456789abcdefghi#authpush",
        "type": "DidAuthPushModeVersion1",
        "serviceEndpoint": "http://auth.example.com/did:example:123456789abcdefg"
    },
    {
        "id": "did:sov:55GkHamhTU1ZbTbV2ab9DE#eidas",
        "type": "EidasService",
        "serviceEndpoint": "http://service_endpoint.sample/did:sov:55GkHamhTU1ZbTbV2ab9DE/eidas"
    }
]

did_doc_services_no_eidas = [
    {
        "id": "did:example:123456789abcdefghi#openid",
        "type": "OpenIdConnectVersion1.0Service",
        "serviceEndpoint": "https://openid.example.com/"
    }, 
    {
        "id": "did:example:123456789abcdefghi#vcr",
        "type": "CredentialRepositoryService",
        "serviceEndpoint": "https://repository.example.com/service/8377464"
    }
]