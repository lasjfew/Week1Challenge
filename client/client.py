from encryption_suite import *
import time

MSG_SIZE = 1024
ENCODER = "utf-8"



def main():

    # asks for input for remote host and remote port
    remote_host, remote_port = [int(i) if i.isdigit() else i for i in
                                input("Enter IP:port of remote connection: ").split(":")]
    
    # Creates a socket and attempts connection with remote server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((remote_host, remote_port))

    # Sends signature for verification by the server
    client_socket.send(sign_ecdsa(b"PENTAGON"))

    # Key exchange
    symmetric_key = key_exchange(client_socket)

    # Continues running communication with symmetric key generated above
    while True:
        
        msg = input("Message: ").encode(ENCODER)

        aad = b"Boo Valinor " + str(time.time()).encode()
        ct, nonce = encrypt_symmetric(msg, symmetric_key, aad)
        client_socket.send(ct)
        client_socket.send(nonce)
        client_socket.send(aad)


if __name__ == "__main__":
    main()

