
 
import socket
import ipaddress
import threading
import time
import contextlib
import errno
from dataclasses import dataclass
import random
import sys
maxPacketSize = 1024
defaultPort = 27017 
global running
serverIP = input('Enter the Ip address of the server: \n')
serverPort = input('Enter the socket for connection: \n')
def GetFreePort(minPort: int = 1024, maxPort: int = 65535):
    for i in range(minPort, maxPort):
        print("Testing port",i)
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as potentialPort:
            try:
                potentialPort.bind((serverIP, i))
                potentialPort.close()
                print("Server listening on port",i)
                return i
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    print("Port",i,"already in use. Checking next...")
                else:
                    print("An exotic error occurred:",e)

def GetServerData() -> list[dict]:
    import mongoDB as mongo
    return mongo.QueryDatabase()

# Method that passes in a list of data generated within IOT devices (document objects) to return a dictionary 
# with key-value pairs of IOT device and ammeter and moisture value
def sensor_data(IOT_data):
    # Initialize the dictionary
    IOTList = {}
    # Iterate through IOT data.
    for data in IOT_data: 
        # Within the data, get the subfields under the field of 'payload'
        keys = data['payload'].keys()
        # Variable to store the sensor name from the payload.
        IOTName = ""
        # Iterate through the subfields of payload
        Ammeter = ""
        MoistureMeter = ""
        for key in keys:
            # loop through keys and if any of them have ammeter in it 
            if "Ammeter" in key:
                # Store the name of it 
                Ammeter = key
            #If moisture is found store it in moistureMeter 
            if "Moisture" in key:
                MoistureMeter = key
        if MoistureMeter == "":
            MoistureMeter = "Capacitive Liquid Level Sensor - Dishwasher Water"
        IOTName = data['payload']['parent_asset_uid']
        if IOTName == 'msp-t57-nb9-sn7':
            IOTName = 'Dishwasher'
        elif IOTName == '8jo-135-4ig-k7o':
            IOTName = 'Refrigeator One'
        else:
            IOTName = 'Refrigerator Two'

        # Get the electricity usage from Ammeter
        electricity = data['payload'][Ammeter]
        # If that IOT device name is already in the dictionary IOTList...
        if (IOTName in IOTList.keys()):
            # We append the list of data for that particular devices.
            IOTList[IOTName].append(data['payload'][Ammeter],data['payload'][MoistureMeter])
        # If that sensor name is not in the list...
        else:
            IOTList[IOTName] = [data['payload'][Ammeter],data['payload'][MoistureMeter]]
    # Return the dictionary of IOT and their list of Ammeter and Moisture Measurement
    return IOTList


# Method that takes IOT list information and returns average moisture within 3hours
def calc_moisture(IOTList):
    avg = 0
    return avg

running = True
def ListenOnTCP(connectionSocket, clientAddress):

    running = True
    print("Connection from:", clientAddress)
    try:
        # Loop to run.
        while running:
            # Recieve message from client.
            clientMessage = connectionSocket.recv(maxPacketSize).decode()
            # If not message break from loop.
            if not clientMessage:
                break
            # Print the client message.
            print("Client message:", clientMessage)

            # Exit by typing exit.
            if clientMessage == "exit":
                print("Exiting Server")
                running = False
                break
            #For all client queries
            if clientMessage =="Moisture":
                # Invoke GetServerData to retrieve data within 3hours.
                IOT_data = GetServerData()

                # If it is retreived 
                if IOT_data:
                    # Invoke sensordata and sensor the IOT data
                    sensorData = sensor_data(IOT_data)
                    # find moisture within 3hours
                    avg = calc_moisture(IOT_data)
                    # Send the average back to the client.
                    serverResponse = connectionSocket.send(bytearray(str(avg), encoding='utf-8'))
    finally:
        connectionSocket.close() # Close the connection
        print(f"Connection with {clientAddress} closed")

def CreateTCPSocket() -> socket.socket:
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcpPort = int(serverPort)  # This will find a free port dynamically
    except Exception as e:
        print("Failed to find a free port: ", e)
        sys.exit(1)  # Exit if no free port is available
    print("TCP Port:", tcpPort)
    tcpSocket.bind((serverIP, tcpPort))
    return tcpSocket


def LaunchTCPThreads():
    tcpSocket = CreateTCPSocket()
    tcpSocket.listen(5)
    while True:
        connectionSocket, connectionAddress = tcpSocket.accept()
        connectionThread = threading.Thread(target=ListenOnTCP, args=[connectionSocket, connectionAddress])
        connectionThread.start()


if __name__ == "__main__":
    tcpThread = threading.Thread(target=LaunchTCPThreads)
    tcpThread.start()

    try:
        while running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Server is shutting down.")
        running = False
        tcpThread.join()   # Wait for the network thread to finish

    print("Server has shut down successfully.")
