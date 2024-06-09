import socket
from ECDH import *
# from TCP_Client import *
from encryption_suite import *

MSG_SIZE = 1024
ENCODER = "utf-8"


def main():
    msg = b''
    private_key = gen_private_key()
    write_private_bytes(private=private_key)

    remote_host, remote_port = [int(i) if i.isdigit() else i for i in input("Enter IP:port of remote connection: ").split(":")]
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((remote_host, remote_port))

# SEND SIGNATURE

    client_socket.send(sign_ecdsa(b"PENTAGON"))

# Key exchange

    symmetric_key = key_exchange(client_socket)

# Symmetrically encrypted communication
    resend = False

    while True:
        if not resend:
            msg = input("Message: ").encode(ENCODER)

        aad = b"Boo Valinor"
        ct, nonce = encrypt_symmetric(msg, symmetric_key, aad)
        client_socket.send(ct)

        # WAIT FOR ACK
        nonce = client_socket.recv(12)
        ct = client_socket.recv(1024)
        msg = decrypt_symmetric(ct, nonce, symmetric_key, aad)
        if msg != "ACK":
            resend = True


if __name__ == "__main__":
    main()

