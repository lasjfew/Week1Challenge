from ecdsa import SigningKey
from hashlib import sha256

private_key = SigningKey.generate(hashfunc=sha256)
public_key = private_key.verifying_key

with open("pub_key.pem", "wb") as f:
    f.write(public_key.to_pem())

with open("priv_key.pem", "wb") as f:
    f.write(private_key.to_pem(format="pkcs8"))

