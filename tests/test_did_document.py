# test_did_document.py

import pytest, json
from eidas_bridge.did_document import DIDDocument, EIDASDIDDocNoSubjectIdException, \
    EIDASServiceEndpointException, _set_eidas_service, _get_services
from demo.data.common_data import did_documents, bad_did_documents, eidas_services, \
        did_doc_services, did_doc_services_no_eidas
from eidas_bridge.eidas_service import EIDASService


def test_did_document_bad_types():
    with pytest.raises(TypeError):
        DIDDocument(bad_did_documents[0])
    with pytest.raises(EIDASDIDDocNoSubjectIdException):
        DIDDocument(json.dumps(bad_did_documents[0]))
    with pytest.raises(EIDASServiceEndpointException):
        DIDDocument(json.dumps(bad_did_documents[1]))

@pytest.mark.parametrize("did_doc", did_documents)
def test_did_document(did_doc):
    str_diddoc = json.dumps(did_doc, indent=4)
    assert DIDDocument(str_diddoc).to_json() == str_diddoc

@pytest.mark.parametrize("did_doc", did_documents)
def test_get_did(did_doc):
    assert DIDDocument(json.dumps(did_doc)).get_did() == did_doc['id']

@pytest.mark.parametrize("did_doc", did_documents)
def test_get_eidas_service_endpoint(did_doc):
    
    expected_service_endpoint = None

    # get eidas service block and then get its endpoint
    for a_service in did_doc['service']:
        if a_service['type'] == EIDASService.EIDAS_SERVICE_TYPE:
            expected_service_endpoint = json.dumps(a_service, indent=1)
    
    output_service_endpoint = DIDDocument(json.dumps(did_doc)).get_eidas_service_endpoint()

    assert output_service_endpoint.to_json() == expected_service_endpoint

@pytest.mark.parametrize("eidas_service", eidas_services)
def test_set_eidas_service(eidas_service):
    output = _set_eidas_service(eidas_service).to_json()
    expected = json.dumps(eidas_service, indent=1)
    assert output == expected

def test_get_services_no_eidas():
    with pytest.raises(EIDASServiceEndpointException):
            _get_services(did_doc_services_no_eidas)

def test_get_services():
    list_services, eidas_service = _get_services(did_doc_services)

    # check eidas service endpoint
    output = eidas_service.to_json()
    expected = json.dumps(eidas_services[0], indent=1)
    assert output == expected

    # check list of services
    i = 0
    for a_service in list_services:
        # check only the three MUST properties (additional properties accepted)
        svc_dict = a_service.to_dict()
        assert svc_dict['id'] == did_doc_services[i]['id']
        assert svc_dict['type'] == did_doc_services[i]['type']
        assert svc_dict['serviceEndpoint'] == did_doc_services[i]['serviceEndpoint']
        i += 1

