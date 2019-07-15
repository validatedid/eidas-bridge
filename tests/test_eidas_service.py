# test_eidas_service.py

import pytest
from eidas_bridge.eidas_service import EIDASService
from tests.data.common_data import all_type_dids, bad_type_endpoints, service_endpoints

@pytest.mark.parametrize("did", all_type_dids)
@pytest.mark.parametrize("service_endpoint", bad_type_endpoints)
def test_EIDASService_class_bad_types(did, service_endpoint):
    with pytest.raises(TypeError):
        EIDASService(did, service_endpoint)

@pytest.mark.parametrize("service_endpoint", service_endpoints)
def test_EIDASService_class(service_endpoint):
    eidas_service = EIDASService(service_endpoint[0], service_endpoint[1])
    assert eidas_service._did == service_endpoint[0]
    assert eidas_service._endpoint == service_endpoint[1]