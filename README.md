# Week1Challenge

This repository contains two folder, client and server. To successfully run this implementation of our encryption suite, one computer should use the client folder and in terminal run
python3 client.py
An example entry for the IP:Port would be 127.0.0.1:12345

While the server computer should likewise use the entire server folder and in terminal run
python3 server.py

Troubleshooting:
The server.py file attempts to use the socket.gethostbyname function so that you do not manually have to enter your IP, but we have had mixed results. Therefore, if running into issues please enter your own IP as a string for the variable HOST_IP in the server.py file. Also, if you wish to change ports you can change the HOST_PORT variable. 

If every message is denied, don't be afraid to change your difference variable, on line 81 of server.py, to a higher number as it your network or computer may be too slow.

If you have any further questions, don't hesitate to reach out to me at crmarettace@gmail.com
