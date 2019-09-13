from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKeyWithSerialization
from cryptography.hazmat.primitives import serialization



def ecdsa_sign(data, private_key) -> bytes:
    signature = private_key.sign(
        data,
        ec.ECDSA(hashes.SHA256())
    )
    return signature

def ecdsa_verify(private_key, signature, data):
    public_key = private_key.public_key()
    serialize_pubkey(public_key)
    public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
    print ("OK")

def serialize_pubkey(public_key) -> bytes:
    serialized_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    print ("Public key:\n")
    print(serialized_public.decode("utf-8"))


if __name__ == '__main__':
    private_key = ec.generate_private_key(
        ec.SECP256K1(), default_backend()
    )
    data = b"This is data to be signed"
    #data2 = b"This is data to be"

    out_sig = ecdsa_sign(data, private_key)
    (r, s) = decode_dss_signature(out_sig)

    print (out_sig)
    print (r)
    print (s)

    ecdsa_verify(private_key, out_sig, data)


