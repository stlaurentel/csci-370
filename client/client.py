import bluetooth
import argparse
import sensorReader
import numpy as np
import RPi.GPIO as GPIO

# use GPIO numbering
GPIO.setmode(GPIO.BCM)
button_pin = 12
GPIO.setup(buttonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

CHUNK_SIZE = 1024

# Create an ArgumentParser to parse the command-line arguments
#parser = argparse.ArgumentParser(description='Bluetooth client script')
#parser.add_argument('server_address', type=str, help='Server Bluetooth device address')
# parser.add_argument('port', type=int, help='Port number to connect to')
# args = parser.parse_args()

# Retrieve the server address and port from the command-line arguments
server_address = "XX:XX:XX:XX:XX:XX"        # format: "XX:XX:XX:XX:XX:XX"
port = 1

client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

try:
    button_state = GPIO.input(button_pin)
    print("Awaiting input...")
    while button_state != 0:
        button_state = GPIO.input(button_pin)
    print("Button pressed! Collecting data now...")
    client_socket.connect((server_address, port))
except bluetooth.btcommon.BluetoothError as e:
    print(f"Bluetooth error: {e}")

# For each piece of data read from sensor, send the data
data_lists = sensorReader.readHeartData(30)
for data in data_lists:
    data_str = np.array2string(data,separator=",")
    bytes_to_send = data_str.encode()

    for i in range(0, len(bytes_to_send), CHUNK_SIZE):
        client_socket.send(bytes_to_send[i:i + CHUNK_SIZE])

client_socket.send("$$$")

data = client_socket.recv(1024)
print(f"Received: {data}")

client_socket.close()
