#dbmanager.py
""" Data storage manager functions to store eIDAS QEC and keys associated with a DID """
import os, csv

class EIDASNotDataCreated(Exception):
    """
    Error raised when no eIDAS Data is already stored.
    """

class DBManager:
    """ Data Storage Manager Class """

    def __init__ (self, file_path="./demo/data/eidas_data.csv"):
        """
        Initialize DBManager instance.

        Args:
            file_path: file in which the data is stored
        """

        self._file_path = file_path

        # check if file exists to prepare the header columns
        if not os.path.exists(self._file_path):
            with open(self._file_path, 'w', newline='') as csvfile:
                fieldnames = ['did', 'certificate', 'private_key', 'password']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
    
    def store_qec(self, did, certificate, privkey, input_password):
        """ Stores the X509 Certificate and its private key with password to a DID indexed file """

        if isinstance(input_password, bytes):
            input_password = bytes(input_password).decode("utf-8")

        with open(self._file_path, 'a', newline='') as csvfile:
                fieldnames = ['did', 'certificate', 'private_key', 'password']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'did': did, 'certificate': certificate, 'private_key': privkey, 'password': input_password})

    def get_qec(self, did) -> str:
        # Gets the Certificate stored in disk associated with the given did
        row = self._get_did_data(did)

        return row['certificate']
    
    def get_key(self, did) -> (str, str):
        # Gets the Key stored in disk associated with the given did 
        row = self._get_did_data(did)

        return row['private_key'], row['password']
    
    def _get_did_data(self, did):
        """ Retrieves the Certificate, Private Key and Password of a specific row from the CSV file indexed by DID """

        with open(self._file_path, "r") as f:
            reader = csv.DictReader(f)
            row = next((item for item in reader if item['did'] == did), None)
        if row is None:
            raise EIDASNotDataCreated("No DID data found. Please add a new certificate, keys, and password associated with its DID.")
        return row
    
    def _delete_last(self):
        """ Deletes last entry on CSV file """
        with open(self._file_path, "r") as f:
            mylist = []
            myreader = csv.DictReader(f)
            headers = myreader.fieldnames
            for row in myreader:
                mylist.append(row)

        # delete last entry
        if len(mylist)>0:
            mylist = mylist[0:-1]
            with open(self._file_path, "w") as fout:
                writer = csv.DictWriter(fout, fieldnames=headers)
                headerdict = dict((col,col) for col in headers)
                writer.writerow(headerdict)
                writer.writerows(mylist)
            


        

    

