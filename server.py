import socket
import encryption_suite
import ecdsa
from ecdsa.keys import SigningKey
import hashlib

HOST_IP = socket.gethostbyname(socket.gethostname())
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
        except AssertionError as e:
            print(f"Error: {e}")
            client_socket.close()


def client_handler(client_socket, client_address):
    print(f"Connection Established with {client_address}")
    # SIGNATURE CONFIRMATION
    client_verify(client_socket)

    # ECDH

    # Symmetrically encrypted communication


def client_verify(client_socket) -> None:

    message = client_socket.recv(128)
    pub_key = client_socket.recv(128)
    signature = client_socket.recv()
    if encryption_suite.verify_signature(message, pub_key, signature):
        return
    else:
        raise AssertionError("Signature verification failed!")
