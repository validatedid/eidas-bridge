# test_dbmanager.py

import pytest, os
from eidas_bridge.utils.dbmanager import DBManager, EIDASNotDataCreated

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
