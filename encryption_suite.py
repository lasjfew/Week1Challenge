from cryptography.hazmat.primitives.ciphers import aead
from cryptography.hazmat.primitives import hashes, hmac
import os
from ECDH import *
import socket


def apply_hmac(key: bytes, msg: bytes) -> bytes:
    h = hmac.HMAC(key, hashes.SHA256()) # Simple function to generate an hmac for key and msg
    h.update(msg)
    return h.finalize()

def create_ecdsa():
    private_key = ec.generate_private_key(ec.SECP384R1())
    with open("./ECDSA", "wb") as f:
        f.write(private_key.private_bytes(Encoding.DER, PrivateFormat.PKCS8, NoEncryption()))


def sign_ecdsa(msg: bytes) -> bytes:
    with open("./ECDSA", "rb") as f:
        private_der = f.read()
        private = load_der_private_key(private_der)
    signature = private.sign(msg, ec.ECDSA(hashes.SHA256()))
    return signature

# Is msg the ct of the original msg?

def verify_signature(msg: bytes, pub_key, signature) -> bool:
    return pub_key.verify(signature, msg, ec.ECDSA(hashes.SHA256()))


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
    private_key = gen_private_key()
    write_private_bytes(private=private_key)
    write_public_bytes(private=private_key)
    public_key = get_public_key()
    client_socket.send(public_key)
    symmetric_key = derive_key(private_key, get_peer_public_key())
    write_aes_key(symmetric_key)
    return symmetric_key
