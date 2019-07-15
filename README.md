eIDAS Bridge Library
====================

This repo contains an implementation of an eIDAS Bridge Library in Python.

An eIDAS Bridge links the european Trust and Legal Framework, named eIDAS (electronic IDentification, Authentication and trust Services), with the Self-Sovereign Identification (SSI) global trust framework, based on Decentralized IDentifers, or DIDs.

Quick Start Guide
=================

#### Requirements

- Python 3.6 or higher
- Cryptograhic libraries with RSA support and X509 capabilities
  - In python use `cryptography`, an easy-to-use library that contains the required crypto & x509 functions:
   ```sh
    $ pip install cryptography
    ```

#### Running the included demo

Clone the repository
```sh
$ git clone https://github.com/validatedid/eidas-bridge
```

Move to the new directory
```sh
$ cd eidas-bridge
```

Create and activate python virtual environment:
```sh
$ python3 -m venv env
$ source env/bin/activate
```

Execute `eidas_demo`:
```sh
$ python eidas_demo.py
```

#### Running Pytest suite tests

##### Requeriments
- Pytest

##### Test execution

```sh
$ pytest
```

eIDAS Bridge Library calls
==========================

#### eidas_link_did
```python
def eidas_link_did(did, certificate, proof, padding = PSS_PADDING) -> str:
```
Link the Issuer DID with eIDAS certificate
Receives a DID, an eIDAS certificate, its proof of possession, and 
optionally the padding of the signature proof (accepts PKCS#1 and PSS)

Returns the JSON that needs to be stored on the Agent public Storage
(i.e: an Identity Hub)

EIDAS Link DID JSON **sample** structure:
```json
{
  "type": "EidasLink",
  "created": "2019-07-11 13:53:50.672317+00:00",
  "did": "did:sov:55GkHamhTU1ZbTbV2ab9DE",
  "certificate": "-----BEGIN CERTIFICATE-----\nMIIDYDCCAkigAwIBAgIUK2iqE3mA/IKP0tw6vZpHu2BDgx0wDQYJKoZIhvcNAQEL\nBQAwXTELMAkGA1UEBhMCRVMxEzARBgNVBAgMClRFU1RfU1RBVEUxEjAQBgNVBAcM\nCVRFU1RfQ0lUWTEQMA4GA1UECgwHQ0FfQUNNRTETMBEGA1UEAwwKbXlzaXRlLmNv\nbTAeFw0xOTA3MDkxNDExMzFaFw0yMDA3MDgxNDExMzFaMF0xCzAJBgNVBAYTAkVT\nMRMwEQYDVQQIDApURVNUX1NUQVRFMRIwEAYDVQQHDAlURVNUX0NJVFkxEDAOBgNV\nBAoMB0NBX0FDTUUxEzARBgNVBAMMCm15c2l0ZS5jb20wggEiMA0GCSqGSIb3DQEB\nAQUAA4IBDwAwggEKAoIBAQCkBTDVrIS8z3xLUvPJgw6KfLQNcAnjUGKCm31D4ug6\nDP/+As6yXyv9ZvantidaqLbvom6RXcbD6b4lohyqr9MZCg7HcFmRiHbovcpPrt05\nPQ5QuFKeKWWEMUGMbXaBVCPb8Q2VbAnw1nzhRspcyDnUhY3HaeeroGpPBra/G+vi\nR5AeOH4WsjSIp7FGJXcd5P6Pizsg5SUyBVMXHeDyBkPp7OEUskyBN6jRnSaCpFZZ\nrKvHHntHIv2f5Q9esfma++bvEhqCGflgiWO+NtCqOs1ueJpPPSLiDQanx7SK5Gyu\n2N8/1mMZsvXR5Ae92eDicIHJdoUyEYmBWr8v1eJvDInfAgMBAAGjGDAWMBQGA1Ud\nEQQNMAuCCWxvY2FsaG9zdDANBgkqhkiG9w0BAQsFAAOCAQEAAnKpcJ64CiXGRw13\nsUnX9xHKSulyNt4BS5LYjoWC1tyQ9FH4kjD5WdFs9VOY89rOwGg1XlpjgJU5tM0i\nuv1J3SPM4ChR81XxxJaJ+ctz4CT2JO1YjLh2daONA9/pTGJgJBa476L9QhkrB1EX\nhRHPeFticEePQEp8lrkdTx4uCdF0FLnPSoh9HUQshDrzSTKW8kWwz7ghu5ZFafmD\nTdjhfyIB1Njvb76qlF1CsJHLD4OxVKXIlaoqOD9qQu42c0tNMfQZpsZI287BjpGm\n/0NrZQ46KDrlewPJdlVXXFEyKJyGnnaU8w8hOmLoNlkFgoCY0GOi6DUgeZ7HVWNf\n2/e1Dw==\n-----END CERTIFICATE-----\n",
  "proof": {
    "type": "RsaSignature2018",
    "padding": "PKCS1-v1_5",
    "signatureValue": "4d91263d4b92042ca110f2a56c7d21eff85d6785c4f743448e7ee2209a41e8807ecabdf5ccf871c1251afa9b17b3cad80d76c3a47999b58656bcb5d5e773793f77be8295d88df4c455fa51fca23ea521e170827b288226d9fad45cc4d9ff87e01646b4b4f5206593dd40d10f76a2f9f3be0a1c4b563c0e9373d639076e250789e183cced5fd23e9e6be1f75025c36a8f9d07c6050ab228e10183e9012fcb896db9186c9093daa5518162a689d1f3a16c43df6d381fe80140509bd3b66b90d5569f895421682953249c2ecebe7209087d2d6f58aff3464d11043bcdf18a28bf666ff1a1020591749fc2833979ceb4ed552a4a756635a6a8db49b0b04b86b7793d"
  }
}
```

#### eidas_get_service_endpoint_struct
```python
def eidas_get_service_endpoint_struct(storage_endpoint) -> str:
```
Contructs the JSON structure that needs to be added to the Issuer's DID Document.
Receives a service endpoint where it is stored the issuer's eIDAS and DID linking information and returns the correspondent JSON.

#### eidas_sign_credential
```python
def eidas_sign_credential(json_credential) -> str:
```
Checks the validity of the issuer's eIDAS certificate against a Trusted Service Provider and adds the corresponde response to the received credential JSON structure.

#### eidas_verify_credential
```python
def eidas_verify_credential(json_credential) -> str:
```
Verifies that the credential issuer had a valid eIDAS certificate at the moment of issuing the passed credential.
Returns: VALID or NOT VALID

REQUISITES
==========

1. DID Document needs to be updated with (a new publickey?? and) a new service endpoint linking to the Identity Hub web service where eIDAS key linkage info is stored.
2. Verifiable Credential needs to be updated with a new service endpoint to check the certificate validity (via an OCSP response or via the stored info of the OCSP response at the moment of issuing the credential)
3. An agent MUST have a storage repository with the capability of exposing a public web service endpoint with access control management (i.e. an Identity Hub)
4. The issuer backoffice MUST implement a PKCS#1 from a given hash
5. The issuer backoffice MUST have an eIDAS certificate.

ROADMAP
=======

### Initial Step
- ~~Code the interface eiDAS Bridge API~~
- ~~Code a demo test~~
- ~~Create a repo on Validated github~~
- ~~Create a Readme.md to explain each API call~~

### Step 0
- Code the Unit test for each API function
- Develop the basic functionality for each API call (no outside interaction)
- Expose the API to an Open API / Swapper REST API

### Step 1
- Add external components: Enterprise Agent (no ledger)

### Step 2
- Add external components: User Agent (no ledger)

### Step 3
- Create a basic web front-end to easy test each API

### Step 4
- Build User Agent UI (to make a real demo)
- Build an Enterprise Agent UI

### Step 5
- Add external components:  Identity Hub

### Step 6
- Add external components:  Sidetree on Ethereum

### Step 7
- Use Verifiable Credentials W3C compatible

### Step 8
- CELEBRATE with :beers:

