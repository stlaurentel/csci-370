import bluetooth
import argparse
import sensorReader
import numpy as np
import RPi.GPIO as GPIO

# use GPIO numbering
GPIO.setmode(GPIO.BCM)
buttonPin = 12
GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)


# Create an ArgumentParser to parse the command-line arguments
parser = argparse.ArgumentParser(description='Bluetooth client script')
parser.add_argument('server_address', type=str, help='Server Bluetooth device address')
parser.add_argument('port', type=int, help='Port number to connect to')
args = parser.parse_args()

# Retrieve the server address and port from the command-line arguments
server_address = args.server_address        # format: "XX:XX:XX:XX:XX:XX"
port = args.port

client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

try:
    buttonState = GPIO.input(buttonPin))
    while buttonState != 1:
        buttonState = GPIO.input(buttonPin))
    
    client_socket.connect((server_address, port))
except bluetooth.btcommon.BluetoothError as e:
    print(f"Bluetooth error: {e}")

# For each piece of data read from sensor, send the data
dataLists = sensorReader.readHeartData(15)
for data in dataLists:
    client_socket.send(np.array2string(data).encode())

data = client_socket.recv(1024)
print(f"Received: {data}")

client_socket.close()
