from cryptography.hazmat.primitives.ciphers import aead
import hashlib
import hmac
from ecdsa.keys import SigningKey, VerifyingKey
import os
from ECDH import *
from socket import socket


def apply_hmac(key: bytes, msg: bytes) -> bytes:
    h = hmac.new(key=key, msg=msg, digestmod=hashlib.sha256) # Simple function to generate an hmac for key and msg
    return h.digest()


def sign_ecdsa(msg: bytes) -> bytes:
    with open("priv_key.pem") as f:
        private_key = SigningKey.from_pem(f.read())

    return private_key.sign(msg)


def verify_signature(msg: bytes, pub_key, signature) -> bool:
    vk = VerifyingKey.from_string(bytes.fromhex(pub_key), hashfunc=hashlib.sha256)
    return vk.verify(bytes.fromhex(signature), msg)


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
