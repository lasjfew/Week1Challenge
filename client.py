from encryption_suite import *
import time
import struct

MSG_SIZE = 1024
ENCODER = "utf-8"



def main():

    remote_host, remote_port = [int(i) if i.isdigit() else i for i in
                                input("Enter IP:port of remote connection: ").split(":")]
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((remote_host, remote_port))

# SEND SIGNATURE
    client_socket.send(sign_ecdsa(b"PENTAGON"))

# Key exchange
    symmetric_key = key_exchange(client_socket)

# Symmetrically encrypted communication
    while True:
        
        msg = input("Message: ").encode(ENCODER)

        aad = b"Boo Valinor " + str(time.time()).encode()
        aad_w_ts = aad + struct.pack('f', time.time())
        # TODO: MAY NEED TO USE COUNTER INSTEAD, AS BOTH SIDES MUST KNOW AAD.. MAYBE

        ct, nonce = encrypt_symmetric(msg, symmetric_key, aad)
        client_socket.send(ct)
        client_socket.send(nonce)
        client_socket.send(aad)


if __name__ == "__main__":
    main()

