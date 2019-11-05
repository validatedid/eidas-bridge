eIDAS Bridge Library
====================

This repo contains an implementation of an eIDAS Bridge Library in Python with a demo and unit tests.

An eIDAS Bridge links the european Trust and Legal Framework, named eIDAS (electronic IDentification, Authentication and trust Services), with the Self-Sovereign Identification (SSI) global trust framework, based on Decentralized IDentifers, or DIDs.

## Table of Contents <!-- omit in toc -->

1. [Run eIDAS Bridge Web Docker Demo](#run-eidas-bridge-web-docker-demo)
2. [Other Running and Test Methods](#other-running-and-test-methods)
3. [eIDAS Bridge Library Calls](#eidas-bridge-library-calls)
4. [Requisites](#requisites)

## Run eIDAS Bridge Web Docker Demo

Move to the base directory (example: `test-eidas-bridge`)
```sh
$ cd test-eidas-bridge
```

Clone the repository and move to the project directory
```sh
$ git clone https://github.com/validatedid/eidas-bridge
$ cd eidas-bridge
```

Execute a script to build and run the dockerized eIDAS Bridge library:
* In \*nix style computers:
```sh
$ ./scripts/build_and_run_docker
```
* In Windows style computers, from a Powershell:
```sh
PS ~\eidas-bridge> bash .\scripts\build_and_run_docker
```

This docker demo exposes a web server to run web demo and also another server to work directly with the eIDAS Bridge Swagger API:
- eIDAS Bridge Web demo on `http://localhost:8080/university_backend/`
- eIDAS Bridge Swagger API on `http://localhost:5002/`

Open your browser and access to `http://localhost:8080/university_backend/` to interact with eIDAS Bridge Web Demo.
Or open your browser and access to `http://localhost:5002/` to interact with the eIDAS Bridge Swagger API.

To stop the demo and docker container, just press `Ctrl^C` on the same terminal your executed the script.

In case you want to use the demo again, there is no need to rebuild the docker, just execute another script to start the already built docker:
```sh
$ ./scripts/start_docker
```
## Other Running and Test Methods

### Install eIDAS Bridge Library

Move to the base directory (example: `test-eidas-bridge`)
```sh
$ cd test-eidas-bridge
```

Clone the repository and move to the project directory
```sh
$ git clone https://github.com/validatedid/eidas-bridge
$ cd eidas-bridge
```

Create and activate python virtual environment:
```sh
$ python3 -m venv env
$ source env/bin/activate
```
Install dependencies and the library into the virtual environment:
```sh
$ pip install -e .
```

If you want to test the demo, install required `requests` library and execute `eidas_demo.py`:
```sh
$ pip install requests
$ python demo/eidas_demo.py
```

### Run Pytest suite tests

Following previous instructions, we should have the project github repo and be placed on `eidas-bridge` directory.

#### Requeriments
- Pytest
- Requests

```sh
$ pip install pytest requests
```

#### Test execution

```sh
$ pytest
```

### Run eIDAS Bridge Library API Demo

Implementation of a demo that exposes a RESTFUL Open API / Swagger style to call eIDAS Bridge Library in Python.
Following previous instructions, we should have the project github repo and be placed on `eidas-bridge` directory.

This demo launches two localhost servers:
- eIDAS Link local data repository on `http://localhost:8000`
- eIDAS Bridge Swagger API on `http://localhost:5002/`

#### Requirements
- Flask
- Flask_RestPLus

```sh
$ pip install install flask flask-restplus
```

#### Running the demo 

Execute `eidas_bridge_api.py`:
```sh
$ python demo/eidas_bridge_api.py
```
SWAGGER API calls will be located at `http://localhost:5002` and will expose:
  - `/eidas/load-qec`
  - `/eidas/service-endpoint`
  - `/eidas/get-pubkey`
  - `/eidas/sign-credential`
  - `/eidas/verify-credential`

## eIDAS Bridge Library calls

#### eidas_load_qec
```python
def eidas_load_qec(did, qec, password = none):
```
Imports an eIDAS Qualified Electronic Certificate (QEC) with its correspondent private key to be used in further digital signature operations.

QEC currently supported format is only **Secp256k1**.

#### eidas_get_service_endpoint
```python
def eidas_get_service_endpoint(did, service_endpoint) -> str:
```
Contructs the JSON structure that needs to be added to the Issuer's DID Document Service Endpoint Section.

Receives a did and a service endpoint where it is stored the issuer's eIDAS Certificate.

Returns the correspondent JSON to be added to the Service Endpoint Section of the Issuer's DID Document.

```json_
{
    "id": "did:sov:55GkHamhTU1ZbTbV2ab9DE#eidas",
    "type": "EidasService",
    "serviceEndpoint": "http://service_endpoint.sample/did:sov:55GkHamhTU1ZbTbV2ab9DE/eidas"
}
```

#### eidas_get_pubkey
```python
def eidas_get_pubkey(did) -> str:
```
From a given DID, returns the correspondent public key in a json struct.

Cryptographic keys currently supported format are only **Secp256k1**.

```json_
{
  "publicKeyPem" : "-----BEGIN PUBLIC KEY...END PUBLIC KEY-----\n"
}
```

#### eidas_sign_credential
```python
def eidas_sign_credential(credential) -> str:
```
Adds a digital signature to the given credential, generated with an eIDAS private key. 

Returns the correspondent Verifiable Credential.

Cryptographic keys currently supported format are only **Secp256k1**.



#### eidas_verify_credential
```python
def eidas_verify_credential(credential, json_did_document):
```
Verifies that the credential issuer had a valid eIDAS certificate at the moment of issuing the passed credential.
Throws `EIDASProofException` on signarure not valid.

The current implementation does NOT support for DID resolution.

The algorithm executes the following procedure:

1. Get DID from the `credential` and from `did_document` and check they are the same
2. Get `EidasService` service endpoint from `did_document` to be able to access the Issuer's Identity Hub
3. Retrieve QEC from the Issuer's Identity Hub, check the certificate validity and extract its public key
4. Verify credential signature with the extracted eIDAS public key 
5. Return `VALID` or throw `EIDASProofException` on signature not valid

## Requisites

1. DID Document needs to be updated with a new public key and service endpoint
2. An agent MUST have a storage repository with the capability of exposing a public web service endpoint with access control management (i.e. an Identity Hub)
3. The issuer backoffice MUST have an eIDAS certificate generated with the following elliptic curve: Secp256k1.


