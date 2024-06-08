from TCP_Client import *
from TCP_Server import *
from ECDH import *

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
peer_public_key = get_peer_public_key()
AES_128_key = derive_key(private_key, peer_public_key)

print(AES_128_key.decode())

#Want to add certificate section here