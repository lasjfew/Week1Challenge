from socket import *
import os
def client_start():
    '''
    Don't want to hardcode port because both need client server 
    connection. Maybe have two separate programs for drone
    versus the server it's communicating with? Not too sure about
    this one. For now leave hardcoded so that we can test connection
    soon.
    '''
    remoteHost = input("Enter IP of remote connection: ")
    remotePort = 12345
    clientSocket = socket(AF_INET, SOCK_STREAM)  # create a TCP socket
    clientSocket.connect((remoteHost, remotePort))  # connect to the server
    return clientSocket

def send_key(clientSocket):
    filename = "ECDH.pub" #HARDCODE with generation
    file = open(('./'+filename), 'rb')  # open the file
    filesize = os.path.getsize('./'+filename)  # get the file size
    encodedFilesize = str(filesize).encode()  # encode the file size
    # pad the file size so we get a 4 byte length felid
    encodedFilesize = ('0' * (4 - len(encodedFilesize))).encode() + encodedFilesize
    clientSocket.send(encodedFilesize)  # send the file size
    header = "ECDH".encode()  # encode the file name
    # pad the action header so we get a 20 byte name field
    header = (' ' * (20 - len(header))).encode() + header
    clientSocket.send(header)  # send the action header
    data = file.read(filesize)  # read first 1024 bytes of the file
    clientSocket.send(data)  # send the data
    file.close()  # close the file

def close_socket(clientSocket, ):
    clientSocket.close()  # close the socket 172.16.181.230