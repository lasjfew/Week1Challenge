import socket
from ECDH import *
from TCP_Client import *
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


# Send certificate (Receive?)

# Key exchange

    #Creates public key and stores and retrieves it
    write_public_bytes(private=private_key)
    public_key = get_public_key()

    #Sends public key to server
    send_key(client_socket)

    #Receive server key and generate

# Symmetrically encrypted communication



if __name__ == "__main__":
    main()

