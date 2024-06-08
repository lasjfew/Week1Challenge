import socket
from ECDH import *
from TCP_Client import *
import encryption_suite
# Sync with server (drone)


def main():
    '''
    Start by generating new keys for ECDHE 
    Should probably make this happen for every exchange
    '''
    private_key = gen_private_key()
    write_private_bytes(private=private_key)

    remoteHost, remotePort = [int(i) if i.isdigit() else i for i in
                              input("Enter IP:port of remote connection: ").split(":")]
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((remoteHost, remotePort))

# SEND SIGNATURE



# Key exchange

    symmetric_key = encryption_suite.key_exchange(client_socket)

# Symmetrically encrypted communication



if __name__ == "__main__":
    main()

