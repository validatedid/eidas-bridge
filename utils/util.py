# util.py
''' Basic functions to help the development '''

import datetime

def timestamp():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat(' ')

def check_args(x, type_x):
    if not isinstance(x, type_x):
        raise TypeError('Please provide a {} argument'.format(type_x))
