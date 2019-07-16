# util.py
''' Auxiliary functions '''

import datetime

def timestamp():
        return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat(' ')

def check_args(x, type_x):
        if not isinstance(x, type_x):
                raise TypeError('Please provide a {} argument'.format(type_x))

def get_did_in_service(uri_did:str) -> str:
        return split_did(uri_did)[0]

def get_fragment_in_service(uri_did:str) -> str:
        return split_did(uri_did)[1]

def split_did(did:str) -> list:
        return did.split('#')


