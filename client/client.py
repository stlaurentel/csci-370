import bluetooth

server_address = "XX:XX:XX:XX:XX:XX"        # replace this with your server's bluetooth MAC address
port = 1                                    # replace this with the port that the server runs on

client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

try:
    client_socket.connect((server_address, port))
except bluetooth.btcommon.BluetoothError as e:
    print(f"Bluetooth error: {e}")

client_socket.send("Hello, server!!!".encode())

data = client_socket.recv(1024)
print(f"Received: {data}")

client_socket.close()
