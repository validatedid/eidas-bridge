# test_dbmanager.py

import pytest, os
from eidas_bridge.utils.dbmanager import DBManager, EIDASNotDataCreated
from demo.data.common_data import all_type_dids

def test_DBManager_class():
    dbmanager = DBManager()

    assert dbmanager._file_path == "./demo/data/eidas_data.csv"
    assert os.path.exists(dbmanager._file_path)

def test_DBManager_path():
    new_path_file = "./demo/data/eidas_data_new.csv"
    dbmanager = DBManager(new_path_file)

    assert dbmanager._file_path == new_path_file
    assert os.path.exists(dbmanager._file_path)

    os.remove(new_path_file)

@pytest.mark.parametrize("did", all_type_dids)
def test_get_did_data_error(did):
    new_path_file = "./demo/data/eidas_data_error.csv"
    dbmanager = DBManager(new_path_file)

    with pytest.raises(EIDASNotDataCreated):
        dbmanager._get_did_data(did)

    os.remove(new_path_file)
