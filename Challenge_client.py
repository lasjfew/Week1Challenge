from TCP_Client import *
from ECDH import *
from encryption_suite import *
'''

'''

#Start server for receiving and client for sending
#Make server async??
clientSocket = client_start()

#Generate keys and save to files
private_key = gen_private_key()
write_private_bytes(private=private_key)
write_public_bytes(private=private_key)
public_key = get_public_key()

#Generate shared AES-128 key using ECDH
send_key(clientSocket=clientSocket)
with open("./PeerECDH.pub", "wb") as g:
    peer_private = gen_private_key()
    g.write(peer_private.public_key().public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo))

peer_public_key = get_peer_public_key()
AES_128_key = derive_key(private_key, peer_public_key)
write_AES_key(AES_128_key)

# with open("./AES_128", "rb") as f:
#     AES_128_key = f.read()
aad = "Valinor Sucks"
msg = "This shit work?"
ct, iv = encrypt_symmetric(msg.encode(), AES_128_key, aad.encode())
print("The cipher text is: ", ct, "\nThe iv is: ", iv)

pt = decrypt_symmetric(ct, iv, AES_128_key, aad.encode())
print(pt.decode())   

#Want to add certificate section here
# 127.0.0.1