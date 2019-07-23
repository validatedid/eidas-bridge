eIDAS Bridge Library
====================

This repo contains an implementation of an eIDAS Bridge Library in Python with a demo and unit tests.

An eIDAS Bridge links the european Trust and Legal Framework, named eIDAS (electronic IDentification, Authentication and trust Services), with the Self-Sovereign Identification (SSI) global trust framework, based on Decentralized IDentifers, or DIDs.

## Table of Contents <!-- omit in toc -->

1. [Run eIDAS Bridge Docker Demo](#run-eidas-bridge-docker-demo)
2. [Other Running and Test Methods](#other-running-and-test-methods)
3. [eIDAS Bridge Library Calls](#eidas-bridge-library-calls)
4. [Requisites](#requisites)
5. [Roadmap](#roadmap)

## Run eIDAS Bridge Docker Demo

Move to the base directory (example: `test-eidas-bridge`)
```sh
$ cd test-eidas-bridge
```

Clone the repository and move to the project directory
```sh
$ git clone https://github.com/validatedid/eidas-bridge
$ cd eidas-bridge
```

Execute a script to build and run the dockerized eIDAS Bridge library
```sh
$ ./scripts/build_and_run_docker
```
This docker demo exposes a server with the eIDAS Bridge Swagger API:
- eIDAS Bridge Swagger API on `http://0.0.0.0:5002/`

Open your browser and access to `http://0.0.0.0:5002/` to interact with the eIDAS Bridge Swagger API.

In case you want to use the demo again, there is no need to rebuild the docker, just execute another script:
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
- eIDAS Bridge Swagger API on `http://127.0.0.1:5002/`

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
  - `/eidas/link-did`
  - `/eidas/service-endpoint`
  - `/eidas/sign-credential`
  - `/eidas/verify-credential`

## eIDAS Bridge Library calls

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
  "certificate": "-----BEGIN CERTIFICATE-----\n...",
  "proof": {
    "type": "RsaSignature2018",
    "padding": "PKCS1-v1_5",
    "signatureValue": "4d91263d4b92042ca110f..."
  }
}
```

#### eidas_get_service_endpoint
```python
def eidas_get_service_endpoint(did, service_endpoint) -> str:
```
Contructs the JSON structure that needs to be added to the Issuer's DID Document Service Endpoint Section.

Receives a did and a service endpoint where it is stored the issuer's eIDAS and DID linking information.

Returns the correspondent JSON to be added to the Service Endpoint Section of the Issuer's DID Document.

```json_
{
    // used to retrieve eIDAS Link data associated with the DID
    "id": "did:sov:55GkHamhTU1ZbTbV2ab9DE#eidas",
    "type": "EidasService",
    "serviceEndpoint": "http://service_endpoint.sample/did:sov:55GkHamhTU1ZbTbV2ab9DE/eidas"
}
```

#### eidas_sign_credential (Not Supported at this Phase 0.)
```python
def eidas_sign_credential(json_credential) -> str:
```
Checks the validity of the issuer's eIDAS certificate against a Trusted Service Provider and adds the corresponde response to the received credential JSON structure.

Raises an `EIDASNotSupportedException` with the following text:`eIDAS library call NOT supported.`

#### eidas_verify_credential
```python
def eidas_verify_credential(json_credential, json_did_document):
```
Verifies that the credential issuer had a valid eIDAS certificate at the moment of issuing the passed credential.
Throws `EIDASProofException` on signarure not valid.

The current implementation does NOT support for DID resolution.

The algorithm executes the following procedure:

1. Get DID from the `json_credential` and from `did_document` and check they are the same
2. Get `EIDASLink` service endpoint from `did_document`
3. Retrieve the EIDAS Link json structure and check that the DID correspond to the one from `did_document`
4. Verify signature with the public key of the EIDAS Link and the proof that contains
5. Return `VALID` or throw `EIDASProofException` on signature not valid

## Requisites

1. DID Document needs to be updated with a new service endpoint linking to the Identity Hub web service where eIDAS key linkage info is stored.
2. An agent MUST have a storage repository with the capability of exposing a public web service endpoint with access control management (i.e. an Identity Hub)
3. The issuer backoffice MUST implement a PKCS#1 from a given hash (Padding supported: PKCS#1 and PSS)
4. The issuer backoffice MUST have an eIDAS certificate (RSA keys with 2048 or 4096 lenght).

## Roadmap

### Initial Step
- ~~Code the interface eiDAS Bridge API~~
- ~~Code a demo test~~
- ~~Create a repo on Validated github~~
- ~~Create a Readme.md to explain each API call~~

### Step 0
- ~~Code the Unit test for each API function~~
- ~~Develop the basic functionality for each API call (no outside interaction)~~
- ~~Expose the API to an Open API / Swapper REST API~~

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

