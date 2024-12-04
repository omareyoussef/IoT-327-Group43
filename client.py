import socket
import ipaddress
import threading
import time
import contextlib
import errno

maxPacketSize = 1024
defaultPort = 27017 
serverIP = '127.0.0.1' 

tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
try:
    tcpPort = int(input("Please enter the TCP port of the host: \n"));
except:
    tcpPort = 0
if tcpPort == 0:
    tcpPort = defaultPort
serverIP = input('Enter the Ip address of the server: \n')
tcpSocket.connect((serverIP, tcpPort))

clientMessage = ""
while clientMessage != "exit":
    clientMessage = input("Available Options : \n1. Moisture\n2.Water Consumption\n3.Electricity (Or type \"exit\" to exit):\n>");

    # Send the message to your server
    tcpSocket.send(bytearray(clientMessage,  encoding="utf-8"))
    
    if clientMessage == "1":
        # Receive a reply from the server for the best highway to take
        serverResponse = tcpSocket.recv(maxPacketSize).decode()
        print(f"Average Moisutre selected.: {serverResponse}")
    else:
        # If the message is not a query, just echo back the server's response
        echoResponse = tcpSocket.recv(maxPacketSize).decode()
        print(f"Server echoed: {echoResponse}")
    
tcpSocket.close()