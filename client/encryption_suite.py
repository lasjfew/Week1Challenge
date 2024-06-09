from cryptography.hazmat.primitives.ciphers import aead
from cryptography.hazmat.primitives.serialization import load_der_private_key, Encoding, PrivateFormat, NoEncryption, \
    PublicFormat
import os
from ECDH import *
import socket

# Used once to create the ECDSA key for the server
# Could be used to create a pair when initially setting up server
# However two keys are included for example usage
def create_ecdsa():
    private_key = ec.generate_private_key(ec.SECP384R1())
    with open("./ECDSA", "wb") as f:
        f.write(private_key.private_bytes(Encoding.DER, PrivateFormat.PKCS8, NoEncryption()))
    with open("./ECDSA.pub", "wb") as g:
        g.write(private_key.public_key().public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo))


# Signs the message with the ecdsa private key for verification
def sign_ecdsa(msg: bytes) -> bytes:
    with open("./ECDSA", "rb") as f:
        private_der = f.read()
        private = load_der_private_key(private_der, None)
    signature = private.sign(msg, ec.ECDSA(hashes.SHA256()))
    return signature


# Verifies the signature by checking hardcoded message with unencrypted version
def verify_signature(msg: bytes, pub_key, signature) -> bool:
    pub_key.verify(signature, msg, ec.ECDSA(hashes.SHA256()))


# Creates a new nonce, uses key, nonce, and aad to encrypt with AES-GCM
# Returns ciphertext and nonce to send to server
def encrypt_symmetric(msg: bytes, key: bytes, aad: bytes) -> tuple[bytes, bytes]:
    nonce = os.urandom(12)
    aesgcm = aead.AESGCM(key)
    ct = aesgcm.encrypt(nonce, msg, aad)
    return ct, nonce

# Decrypts messages using AES-GCM
def decrypt_symmetric(ct: bytes, nonce: bytes, key: bytes, aad: bytes) -> bytes:
    aesgcm = aead.AESGCM(key)
    pt = aesgcm.decrypt(nonce, ct, aad)
    return pt

# The key exchange that occurs on both the client and server side
def key_exchange(client_socket: socket) -> bytes:

    # Generates a private key
    private_key = gen_private_key()

    # Makes public key from private key
    public_key = private_key.public_key()

    # Shares new public information with other side
    client_socket.send(public_key.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo))
    
    # Receives other side's public key
    peer_public_key = client_socket.recv(1024)

    # Uses peer's public key and own private key to create a shared symmetric key
    symmetric_key = derive_key(private_key, load_der_public_key(peer_public_key))

    # Returns AES-128 key
    return symmetric_key
