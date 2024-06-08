import socket

# Sync with server (drone)


def main():
    remoteHost, remotePort = [int(i) if i.isdigit() else i for i in
                              input("Enter IP:port of remote connection: ").split(":")]
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((remoteHost, remotePort))


# Send certificate

# Key exchange

# Symmetrically encrypted communication


if __name__ == "__main__":
    main()

