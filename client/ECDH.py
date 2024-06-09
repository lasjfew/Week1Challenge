from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.asymmetric import ec

from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from cryptography.hazmat.primitives.serialization import load_der_public_key

# Generates a private key for ECC using the P384 curve
def gen_private_key():
    private = ec.generate_private_key(ec.SECP384R1())
    return private


# Grabs public key for server to verify client
def get_peer_public_key_ecdsa():
    with open("./ECDSA.pub", "rb") as g:
        data = g.read()
        public = load_der_public_key(data)
    return public




# Generates shared symmetric key using HKDF and exchanged information
def derive_key(private, peer_public):
    shared_key = private.exchange(ec.ECDH(), peer_public)

    # HKDF is used because distribution of bits in
    # ECDH shared keys is not uniform
    derived_key = HKDF(algorithm=hashes.SHA256(), length=32, salt=b'', info=b'', ).derive(shared_key)
    return derived_key




