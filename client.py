'''
Notes:
    Do we generate a new iv each time?
    Should be count with iv and not regenerate
    ECDHE maybe?
    Send new aad everytime with timestamp. After decryption check that time is within
    10ms?, so only so many packets can be sent?
'''


from encryption_suite import *

MSG_SIZE = 1024
ENCODER = "utf-8"


def main():

    remote_host, remote_port = [int(i) if i.isdigit() else i for i in
                                input("Enter IP:port of remote connection: ").split(":")]
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((remote_host, remote_port))

# SEND SIGNATURE

    client_socket.send(sign_ecdsa(b"PENTAGON"))

# Key exchange

    symmetric_key = key_exchange(client_socket)

# Symmetrically encrypted communication

    while True:
        
        msg = input("Message: ").encode(ENCODER)

        aad = b"Boo Valinor"
        ct, nonce = encrypt_symmetric(msg, symmetric_key, aad)
        client_socket.send(ct)
        client_socket.send(nonce)


if __name__ == "__main__":
    main()

