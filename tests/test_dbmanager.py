# test_dbmanager.py

import pytest, os, csv
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
    new_path_file = "./demo/data/eidas_data_test1.csv"
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
    new_path_file = "./demo/data/eidas_data_test2.csv"
    dbmanager = DBManager(new_path_file)

    dbmanager.store_qec(eidas_data[0], eidas_data[1], eidas_data[2], eidas_data[3])
    qec = dbmanager.get_qec(eidas_data[0])
    assert qec == eidas_data[1]
    os.remove(new_path_file)

@pytest.mark.parametrize("eidas_data", eidas_data_list)
def test_get_key(eidas_data):
    new_path_file = "./demo/data/eidas_data_test3.csv"
    dbmanager = DBManager(new_path_file)

    dbmanager.store_qec(eidas_data[0], eidas_data[1], eidas_data[2], eidas_data[3])
    privkey, password = dbmanager.get_key(eidas_data[0])
    assert privkey == eidas_data[2]
    assert password == eidas_data[3]
    os.remove(new_path_file)

@pytest.mark.parametrize("eidas_data", eidas_data_list)
def test_store_qec(eidas_data):
    new_path_file = "./demo/data/eidas_data_test4.csv"
    dbmanager = DBManager(new_path_file)

    dbmanager.store_qec(eidas_data[0], eidas_data[1], eidas_data[2], eidas_data[3])
    row = dbmanager._get_did_data(eidas_data[0])
    assert row['did'] == eidas_data[0]
    assert row['certificate'] == eidas_data[1]
    assert row['private_key'] == eidas_data[2]
    assert row['password'] == eidas_data[3]
    os.remove(new_path_file)

@pytest.mark.parametrize("eidas_data", eidas_data_list)
def test_store_qec_pass(eidas_data):
    new_path_file = "./demo/data/eidas_data_test6.csv"
    new_password = b'this is a byte password'
    decoded_new_password = 'this is a byte password'
    dbmanager = DBManager(new_path_file)

    dbmanager.store_qec(eidas_data[0], eidas_data[1], eidas_data[2], new_password)
    row = dbmanager._get_did_data(eidas_data[0])
    assert row['did'] == eidas_data[0]
    assert row['certificate'] == eidas_data[1]
    assert row['private_key'] == eidas_data[2]
    assert row['password'] == decoded_new_password
    os.remove(new_path_file)

@pytest.mark.parametrize("eidas_data", eidas_data_list)
def test_delete_last(eidas_data):
    new_path_file = "./demo/data/eidas_data_test5.csv"
    dbmanager = DBManager(new_path_file)
    # store an entry
    dbmanager.store_qec(eidas_data[0], eidas_data[1], eidas_data[2], eidas_data[3])
    assert count_lines(new_path_file) == 1
    # delete last entry
    dbmanager._delete_last()
    assert count_lines(new_path_file) == 0

    os.remove(new_path_file)


def count_lines(file_path) -> int:
    mylist = []
    with open(file_path, "r") as f:
        myreader = csv.DictReader(f)
        for row in myreader:
            mylist.append(row)
    return len(mylist)