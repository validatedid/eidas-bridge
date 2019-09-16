# test_eidas_service.py

import pytest, json, multiprocessing
from eidas_bridge.eidas_service import EIDASService
from eidas_bridge.did_document import DIDDocument
from demo.data.common_data import all_type_dids, bad_type_endpoints, service_endpoints, \
    eidas_services
from eidas_bridge.utils.util import clean_did
from demo.util.hub_server import start_hub_server

@pytest.mark.parametrize("did", all_type_dids)
@pytest.mark.parametrize("service_endpoint", bad_type_endpoints)
def test_EIDASService_class_bad_types(did, service_endpoint):
    with pytest.raises(TypeError):
        EIDASService(did, service_endpoint)

@pytest.mark.parametrize("eida_service", eidas_services)
def test_EIDASService_class(eida_service):
    out_service = EIDASService(eida_service['id'], eida_service['serviceEndpoint'])
    assert out_service._did == clean_did(eida_service['id'])
    assert out_service._endpoint == eida_service['serviceEndpoint']

@pytest.mark.parametrize("eida_service", eidas_services)
def test_EIDASService_compare_jsons(eida_service):
    expected_json = json.dumps(eida_service, indent=1)
    output_json = EIDASService(
        eida_service['id'], 
        eida_service['serviceEndpoint']
        ).to_json()
    assert expected_json == output_json

@pytest.mark.parametrize("eida_service", eidas_services)
def test_get_endpoint(eida_service):
    out_service = EIDASService(eida_service['id'], eida_service['serviceEndpoint'])
    assert out_service.get_endpoint() == eida_service['serviceEndpoint']