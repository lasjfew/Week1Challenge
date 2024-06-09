import socket
import encryption_suite
from ECDH import *
import time

# Grabs IP with socket library, otherwise hardcodes values
HOST_IP = socket.gethostbyname(socket.gethostname())
HOST_PORT = 54321
MSG_SIZE = 1024
ENCODER = "utf-8"
server_running = True


def main():
    global server_running

    # Starts server listening for connections

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST_IP, HOST_PORT))
    server_socket.listen(1)


    while server_running:
        
        # Accepts connection from client

        client_socket, client_address = server_socket.accept()

        # Verification step for client
        try:
            client_handler(client_socket, client_address)

        #If not verified, closes connection with client and prints error

        except Exception as e:
            print(f'Error is {e}')
            print(f"Not verified, socket closing\n" + "-"*25)
            client_socket.close()

# Handles the client connection

def client_handler(client_socket, client_address):
    print(f"Connection Established with {client_address}")

    # Signature verfication

    client_verify(client_socket)
    print("Verified!")

    # ECDH key exchange

    symmetric_key = encryption_suite.key_exchange(client_socket)
    print("Keys Exchanged!")

    # Symmetrically encrypted communication

    while True:
        # msg is received ciphertext
        msg = client_socket.recv(MSG_SIZE)
        nonce_and_aad = client_socket.recv(MSG_SIZE)

        #Splits up the nonce and AAD

        nonce = nonce_and_aad[:12]
        aad = nonce_and_aad[12:]

        # Prints if message is not the empty string
        if msg:
            print(f"Message received from {client_address}")

        # Decryption step
        pt = encryption_suite.decrypt_symmetric(msg, nonce, symmetric_key, aad)

        # Grabs timestamp from the aad as first 12 chars are hardcoded
        ts = float(aad.decode()[12:])

        # Grabs current time and makes sure the message 
        # was sent within the viable window
        
        cur_time = time.time()
        difference = cur_time-ts
        if difference> 0.13:
            print("Message denied, took ", difference, " seconds to receive")
        else:
            print("Message accepted")
            print(pt.decode(ENCODER))
        
        
        


def client_verify(client_socket) -> None:

    # Receives enough bytes to read the full signature
    signature = client_socket.recv(150)

    # Hardcoded message here
    message = b"PENTAGON"

    # Runs verify_signature() from encryption_suite
    encryption_suite.verify_signature(message, get_peer_public_key_ecdsa(), signature)

if __name__ == "__main__":
    main()