import socket
import encryption_suite
from ECDH import *

HOST_IP = "192.168.0.171" #socket.gethostbyname(socket.gethostname())
HOST_PORT = 12345
MSG_SIZE = 1024
ENCODER = "utf-8"
server_running = True


def main():
    global server_running
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST_IP, HOST_PORT))
    server_socket.listen(1)

    while server_running:
        client_socket, client_address = server_socket.accept()
        try:
            client_handler(client_socket, client_address)
        except Exception as e:
            print(f'Error is {e}')
            print(f"Not verified, socket closing\n" + "-"*25)
            client_socket.close()


def client_handler(client_socket, client_address):
    print(f"Connection Established with {client_address}")

    # SIGNATURE CONFIRMATION
    client_verify(client_socket)
    print("Verified!")

    # ECDH
    symmetric_key = encryption_suite.key_exchange(client_socket)
    print("Keys Exchanged!")

    # Symmetrically encrypted communication
    while True:
        msg = client_socket.recv(MSG_SIZE)
        nonce = client_socket.recv(MSG_SIZE)
        if msg:
            print(f"Message received from {client_address}")
        aad = b"Boo Valinor"
        pt = encryption_suite.decrypt_symmetric(msg, nonce, symmetric_key, aad)
        print(pt.decode(ENCODER))


def client_verify(client_socket) -> None:

    signature = client_socket.recv(150)
    print(signature)
    # Hardcoded message here
    message = b"PENTAGON"
    encryption_suite.verify_signature(message, get_peer_public_key_ecdsa(), signature)
    print("Done with verification")


if __name__ == "__main__":
    main()