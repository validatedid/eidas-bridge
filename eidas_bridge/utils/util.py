# util.py
""" Auxiliary functions """
""" some functions extracted from https://github.com/hyperledger/aries-cloudagent-python/blob/master/aries_cloudagent/messaging/connections/models/diddoc/util.py """


import datetime

def timestamp():
        return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat(' ')

def check_args(x, type_x):
        if not isinstance(x, type_x):
                raise TypeError('Please provide a {} argument'.format(type_x))

def get_did_in_service(uri_did:str) -> str:
        return resource(uri_did)[0]

def get_fragment_in_service(uri_did:str) -> str:
        return resource(uri_did)[1]

#def split_did(did:str) -> list:
#        return did.split('#')


def clean_did(ref: str) -> str:
    """ extract the resource for an identifier, 
        using '#', ';' and '?' as possible delimiters
    """
    # default delimiter '#'
    did1 = resource(ref)[0]
    # delimiter ';'
    did2 = resource(did1, ';')[0]
    # delimiter '?'
    return resource(did2, '?')[0]
    

def resource(ref: str, delimiter: str = None) -> list:
    """
    Extract the resource for an identifier.

    Given a (URI) reference, return up to its delimiter and also the rest

    Args:
        ref: reference
        delimiter: delimiter character
            (default None maps to '#', or ';' introduces identifiers)
    """

    return ref.split(delimiter if delimiter else "#")


