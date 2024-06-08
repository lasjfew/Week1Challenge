from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import hashlib
import hmac
from ecdsa import SigningKey
import os


def apply_hmac(key: bytes, msg: bytes) -> bytes:
    h = hmac.new(key=key, msg=msg, digestmod=hashlib.sha256) # Simple function to generate an hmac for key and msg
    return h.digest()


def sign_ecdsa(msg: bytes) -> bytes:
    sk = SigningKey.generate() # Generate SigningKey object

    # Can verify with vk = sk.verifying_key, vk.verify(signature, b'message')
    return sk.sign(msg)


def encrypt_symmetric(msg: bytes, key: bytes) -> (bytes, bytes):
    iv = os.urandom(16)
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv)
    ).encryptor()
    ct = encryptor.update(msg)
    return ct, iv


def decrypt_symmetric(ct: bytes, iv: bytes, key: bytes) -> bytes:
    decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    decryptor.update(ct)
    return decryptor.finalize()
