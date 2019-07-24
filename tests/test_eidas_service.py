# test_eidas_service.py

import pytest, json, multiprocessing
from eidas_bridge.eidas_service import EIDASService
from eidas_bridge.did_document import DIDDocument
from eidas_bridge.eidaslink import EIDASLink
from demo.data.common_data import all_type_dids, bad_type_endpoints, service_endpoints, \
    eidas_services, eidas_link_and_diddocs_jsons
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

def test_get_eidas_link_did():
    # run server daemon thread
    hub_server_proc = multiprocessing.Process(target=start_hub_server)
    hub_server_proc.start()

    # getting the first element that is the one it is saved in the server
    input_struct = eidas_link_and_diddocs_jsons[0]

    # get eidas service from the did doc and retrieve the eidas link structure
    did_doc = DIDDocument(input_struct[0])
    eidas_service = did_doc.get_eidas_service_endpoint()
    eidas_link_output = eidas_service.get_eidas_link_did()

    # json eidas link expected
    eidas_link_expected = json.dumps(input_struct[1], indent=2)

    assert eidas_link_output == eidas_link_expected