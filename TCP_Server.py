from socket import *

def server_start():
    '''
    This could be automated for sure and should be
    '''
    serverHost = input("Enter IP of host: ")
    serverPort = 12345

    serverSocket = socket(AF_INET, SOCK_STREAM) #Creates a streaming socket
    serverSocket.bind((serverHost, serverPort)) #Binds the socket to the IP ad Port number
    serverSocket.listen(1) #Starts listening for data
    while True:
        print("server ready to receive")
        connectionSocket, addr = serverSocket.accept() #Socket accepts the request and sends to the connection socket they will communicate over
        size = int(connectionSocket.recv(4).decode()) #Reads in the size of the data
        action = connectionSocket.recv(20).decode().strip() #Reads in the file name, omitting extra spaces
        '''
        add some logic for action 
        (ECDH, AES, Certificate Check, Certificate Verify?)
        '''
        with open("PeerECDH.pub", "wb+") as f: #Opens the new file to write to in a new directory
            data_input = connectionSocket.recv(size) #File data is read in
            f.write(data_input) #File data is written to the file