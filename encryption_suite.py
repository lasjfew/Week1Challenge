from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import hashlib
import hmac
from ecdsa.keys import SigningKey, VerifyingKey
import os


def apply_hmac(key: bytes, msg: bytes) -> bytes:
    h = hmac.new(key=key, msg=msg, digestmod=hashlib.sha256) # Simple function to generate an hmac for key and msg
    return h.digest()


def sign_ecdsa(key: bytes, msg: bytes) -> (bytes, bytes):
    private_key = SigningKey.generate(hashfunc=hashlib.sha256()) # Generate SigningKey object
    verifying_key = private_key.get_verifying_key()

    return private_key.sign(msg), verifying_key


def verify_signature(msg: bytes, pub_key, signature) -> bool:
    vk = VerifyingKey.from_string(bytes.fromhex(pub_key), hashfunc=hashlib.sha256)
    return vk.verify(bytes.fromhex(signature), msg)


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
