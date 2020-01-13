![EBSI Logo](https://ec.europa.eu/cefdigital/wiki/images/logo/default-space-logo.svg)

# eIDAS Bridge Library
> The library linking SSI with eIDAS

An eIDAS Bridge links the european Trust and Legal Framework, named eIDAS (electronic IDentification, Authentication and trust Services), with the Self-Sovereign Identification (SSI) global trust framework, based on Decentralized IDentifers, or DIDs.

## Table of Contents

1. [Getting started](#Getting)
2. [Building](#Building)
3. [Testing](#Testing)
4. [Running](#Running)
5. [Features](#Features)
6. [Requisites](#Requisites)
6. [Licensing](#Licensing)


## Getting started

### Prerequisites
Required libraries:

- typescript


### Installing

Move to the base directory (example: `test-eidas-bridge`)
```sh
$ cd test-eidas-bridge
```

Clone the repository and move to the project directory
```sh
$ git clone https://<your_user>@ec.europa.eu/cefdigital/code/scm/ebsi/4-eidas-bridge.git
$ cd 4-eidas-bridge
```
### Docker
Execute a script to build and run the dockerized eIDAS Bridge library:

```sh
$ docker-compose up --build  
```

This docker demo exposes a server to work directly with the eIDAS Bridge Swagger API:
- eIDAS Bridge Swagger API on `http://localhost:5002/`

Open your browser and access to `http://localhost:5002/` to interact with the eIDAS Bridge Swagger API.

To stop the demo and docker container, just press `Ctrl^C` on the same terminal your executed the script.

In case you want to use the demo again, there is no need to rebuild the docker, just execute another script to start the already built docker:
```sh
$ docker-compose up
```


## Building
Move to the base directory (example: `test-eidas-bridge`)
```sh
$ cd test-eidas-bridge
```

Clone the repository and move to the project directory
```sh
$ git clone https://<your_user>@ec.europa.eu/cefdigital/code/scm/ebsi/4-eidas-bridge.git
$ cd 4-eidas-bridge
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
## Testing
Following [previous instructions](#Building), we should have the project github repo and be placed on `eidas-bridge` directory.

### Prerequisites
- Pytest
- Requests

```sh
$ pip install pytest requests
```

### Test execution

```sh
$ pytest
```

## Running
Run eIDAS Bridge Library API Demo

Implementation of a demo that exposes a RESTFUL Open API / Swagger style to call eIDAS Bridge Library in Python.
Following previous instructions, we should have the project github repo and be placed on `eidas-bridge` directory.

This demo launches:
- eIDAS Bridge Swagger API on `http://localhost:5002/`

### Requirements
- Flask
- Flask_RestPLus

```sh
$ pip install install flask flask-restplus
```

### Running the demo 

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
  
## Features
eIDAS Bridge Library calls

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
    "id": "did:ebsi:55GkHamhTU1ZbTbV2ab9DE#eidas",
    "type": "EidasService",
    "serviceEndpoint": "http://service_endpoint.sample/did:ebsi:55GkHamhTU1ZbTbV2ab9DE/eidas"
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


## Licensing

Copyright (c) 2019 European Commission
Licensed under the EUPL, Version 1.2 or - as soon they will be approved by the European Commission - subsequent versions of the EUPL (the "Licence"); 
You may not use this work except in compliance with the Licence. 
You may obtain a copy of the Licence at: 
* https://joinup.ec.europa.eu/page/eupl-text-11-12  

Unless required by applicable law or agreed to in writing, software distributed under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the Licence for the specific language governing permissions and limitations under the Licence.