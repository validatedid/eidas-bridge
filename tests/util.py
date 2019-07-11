# util.py
""" data and functions to better testing """

import base58
import base64

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def b64_to_bytes(val: str, urlsafe=False) -> bytes:
    """Convert a base 64 string to bytes."""
    if urlsafe:
        return base64.urlsafe_b64decode(val)
    return base64.b64decode(val)


def bytes_to_b64(val: bytes, urlsafe=False) -> str:
    """Convert a byte string to base 64."""
    if urlsafe:
        return base64.urlsafe_b64encode(val).decode("ascii")
    return base64.b64encode(val).decode("ascii")


def b58_to_bytes(val: str) -> bytes:
    """Convert a base 58 string to bytes."""
    return base58.b58decode(val)


def bytes_to_b58(val: bytes) -> str:
    """Convert a byte string to base 58."""
    return base58.b58encode(val).decode("ascii")

def print_object(input_obj):
    print("{}".format(input_obj.decode()))