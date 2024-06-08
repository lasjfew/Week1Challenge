import socket
import encryption_suite
from ECDH import *

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

    while True:
        message = client_socket.recv(MSG_SIZE)
        # print(f"Received from {client_address}: {message}")
        encryption_suite.encrypt_symmetric("ACK", symmetric_key, )
        client_socket.send()


def client_handler(client_socket, client_address):
    print(f"Connection Established with {client_address}")
    # SIGNATURE CONFIRMATION
    client_verify(client_socket)

    # ECDH

    symmetric_key = encryption_suite.key_exchange(client_socket)

    # Symmetrically encrypted communication
    '''
    Probably make this a while True to keep entering
    commands to run the drone? Hardcode commands of
    up down left right forwards backwards
    '''
    while True:
        msg = client_socket.recv(MSG_SIZE)
        if msg:
            print(f"Message received from {client_address}")
        aad = b"Boo Valinor"
        msg = b"ACK"
        client_socket.send(encryption_suite.encrypt_symmetric(msg, symmetric_key, aad))


def client_verify(client_socket) -> None:

    message = client_socket.recv(128)
    signature = client_socket.recv()
    if encryption_suite.verify_signature(message, get_peer_public_key(), signature):
        return
    else:
        raise AssertionError("Signature verification failed!")
