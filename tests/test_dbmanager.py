# test_dbmanager.py

import pytest, os
from eidas_bridge.utils.dbmanager import DBManager, EIDASNotDataCreated
from demo.data.common_data import dids, eidas_data_list

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

@pytest.mark.parametrize("did", dids)
def test_get_did_data_error(did):
    new_path_file = "./demo/data/eidas_data_error.csv"
    dbmanager = DBManager(new_path_file)

    with pytest.raises(EIDASNotDataCreated):
        dbmanager._get_did_data(did)

    os.remove(new_path_file)

@pytest.mark.parametrize("eidas_data", eidas_data_list)
def test_get_did_data(eidas_data):
    new_path_file = "./demo/data/eidas_data_ok.csv"
    dbmanager = DBManager(new_path_file)

    dbmanager.store_qec(eidas_data[0], eidas_data[1], eidas_data[2], eidas_data[3])
    row = dbmanager._get_did_data(eidas_data[0])
    assert row['did'] == eidas_data[0]
    assert row['certificate'] == eidas_data[1]
    assert row['private_key'] == eidas_data[2]
    assert row['password'] == eidas_data[3]
    os.remove(new_path_file)

@pytest.mark.parametrize("eidas_data", eidas_data_list)
def test_get_qec(eidas_data):
    new_path_file = "./demo/data/eidas_data_ok.csv"
    dbmanager = DBManager(new_path_file)

    dbmanager.store_qec(eidas_data[0], eidas_data[1], eidas_data[2], eidas_data[3])
    qec = dbmanager.get_qec(eidas_data[0])
    assert qec == eidas_data[1]
    os.remove(new_path_file)

@pytest.mark.parametrize("eidas_data", eidas_data_list)
def test_get_key(eidas_data):
    new_path_file = "./demo/data/eidas_data_ok.csv"
    dbmanager = DBManager(new_path_file)

    dbmanager.store_qec(eidas_data[0], eidas_data[1], eidas_data[2], eidas_data[3])
    privkey, password = dbmanager.get_key(eidas_data[0])
    assert privkey == eidas_data[2]
    assert password == eidas_data[3]
    os.remove(new_path_file)

@pytest.mark.parametrize("eidas_data", eidas_data_list)
def test_store_qec(eidas_data):
    new_path_file = "./demo/data/eidas_data_ok.csv"
    dbmanager = DBManager(new_path_file)

    dbmanager.store_qec(eidas_data[0], eidas_data[1], eidas_data[2], eidas_data[3])
    row = dbmanager._get_did_data(eidas_data[0])
    assert row['did'] == eidas_data[0]
    assert row['certificate'] == eidas_data[1]
    assert row['private_key'] == eidas_data[2]
    assert row['password'] == eidas_data[3]
    os.remove(new_path_file)