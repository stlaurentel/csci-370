import bluetooth
import argparse
import sensorReader


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
    client_socket.connect((server_address, port))
except bluetooth.btcommon.BluetoothError as e:
    print(f"Bluetooth error: {e}")

# For each piece of data read from sensor, send the data
heartData = sensorReader.readHeartData(15)
for dataPoint in heartData:
    client_socket.send(str(dataPoint).encode())

data = client_socket.recv(1024)
print(f"Received: {data}")

client_socket.close()
