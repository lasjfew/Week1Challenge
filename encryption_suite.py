from cryptography.hazmat.primitives.ciphers import aead
import os
from ECDH import *
import socket


def create_ecdsa():
    private_key = ec.generate_private_key(ec.SECP384R1())
    with open("./ECDSA", "wb") as f:
        f.write(private_key.private_bytes(Encoding.DER, PrivateFormat.PKCS8, NoEncryption()))
    with open("./ECDSA.pub", "wb") as g:
        g.write(private_key.public_key().public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo))


def sign_ecdsa(msg: bytes) -> bytes:
    with open("./ECDSA", "rb") as f:
        private_der = f.read()
        private = load_der_private_key(private_der, None)
    signature = private.sign(msg, ec.ECDSA(hashes.SHA256()))
    print(signature)
    return signature


# Is msg the ct of the original msg?

def verify_signature(msg: bytes, pub_key, signature) -> bool:
    pub_key.verify(signature, msg, ec.ECDSA(hashes.SHA256()))


def encrypt_symmetric(msg: bytes, key: bytes, aad: bytes) -> tuple[bytes, bytes]:
    nonce = os.urandom(12)
    aesgcm = aead.AESGCM(key)
    ct = aesgcm.encrypt(nonce, msg, aad)
    return ct, nonce


def decrypt_symmetric(ct: bytes, nonce: bytes, key: bytes, aad: bytes) -> bytes:
    aesgcm = aead.AESGCM(key)
    pt = aesgcm.decrypt(nonce, ct, aad)
    return pt


def key_exchange(client_socket: socket) -> bytes:
    print("What is going on")
    private_key = gen_private_key()
    public_key = private_key.public_key()
    client_socket.send(public_key.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo))
    peer_public_key = client_socket.recv(1024)
    symmetric_key = derive_key(private_key, load_der_public_key(peer_public_key))
    write_aes_key(symmetric_key)
    return symmetric_key
