# util.py
''' Basic functions to help the development '''

def check_args(x, type_x):
    if not isinstance(x, type_x):
        raise TypeError('Please provide a {} argument'.format(type_x))