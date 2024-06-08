import os

from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.asymmetric import ec

from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from cryptography.hazmat.primitives.serialization import NoEncryption

from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, load_der_private_key, load_der_public_key



def gen_private_key():
    private = ec.generate_private_key(ec.SECP384R1())
    return private

# Write public bytes over network to create shared key
# Maybe check to see if folder exists and if so ignore? Otherwise writing to file seems redundant
def write_private_bytes(private):
    with open("ECDH", "wb") as f:
        f.write(private.private_bytes(Encoding("DER"), PrivateFormat("PKCS8"), NoEncryption()))

def write_public_bytes(private):
    with open("ECDH.pub", "wb") as f:
        f.write(private.public_key().public_bytes(Encoding("DER"), PrivateFormat("PKCS8"), NoEncryption()))

'''
Finish this function to interact with socket programming somehow
'''
def get_public_key():
    with open("ECDH.pub", "rb") as g:
        data = g.read()
        public = load_der_public_key(data, password=None)
    return public

def get_peer_public_key():
    with open("PeerECDH.pub", "rb") as g:
        data = g.read()
        public = load_der_public_key(data, password=None)
    return public



'''
Generates shared symmetric key, think about adding info for randomness (e.g. 'Death to Valinor') and 
make sure that HKDFExpand isn't necessary for this module.
'''
def derive_key(private, peer_public):
    shared_key = private.exchange(ec.ECDH(), peer_public)
    derived_key = HKDF(algorithm=hashes.SHA256(),length=128,salt=b'',info=b'',).derive(shared_key)
    return derived_key
        
'''
Don't need this function as derive_key generates AES key
'''
def encrypt_ECDH(derived_key, msg):
    encrypted_data = derived_key.encrypt(msg.encode())
    return encrypted_data

# Socket programming here
'''
shared = private.exchange(ec.ECDH(), public)



WHAT THE FUCK IS THIS

https://soatok.blog/2021/11/17/understanding-hkdf/

And what do I do after this
'''

# derived = HKDF(algorithm=hashes.SHA256(),length=32,salt=b'',info=b'',).derive(shared)

