import socket
import encryption_suite
from ECDH import *

HOST_IP = "127.0.0.1" #socket.gethostbyname(socket.gethostname())
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
        except:
            print(f"Not verified, socket closing\n" + "-"*25)
            client_socket.close()


def client_handler(client_socket, client_address):
    print(f"Connection Established with {client_address}")
    # SIGNATURE CONFIRMATION
    client_verify(client_socket)
    print("Verified!")
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
        # TODO: ADD HMAC CODE BEFORE ACKNOWLEDGING
        ct, nonce = encryption_suite.encrypt_symmetric(msg, symmetric_key, aad)
        client_socket.send(nonce)
        client_socket.send(ct)

#client verif in server file???
def client_verify(client_socket) -> None:

    signature = client_socket.recv(150)
    print(signature)
    # Hardcoded message here
    message = b"PENTAGON"
    encryption_suite.verify_signature(message, get_peer_public_key_ecdsa(), signature)

if __name__ == "__main__":
    main()