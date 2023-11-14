#define PY_SSIZE_T_CLEAN 1
import bluetooth
import numpy as np
import ast
import re
import csv


server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(("", bluetooth.PORT_ANY))  # Bind to any available port for RFCOMM
server_socket.listen(1)  # Listen for one incoming connection

port = server_socket.getsockname()[1]  # Get the dynamically assigned port

print(f"Waiting for a Bluetooth connection on port {port}...")

client_socket, client_address = server_socket.accept()
print(f"Accepted connection from {client_address}")

# Receive data from the client
try:
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        dataString = data.decode()
        # dataString format: "['11/13/23 19:32:19' 'HR2' 'external' '100.0' '100.0' '100.0']['11/13/23 19:32:19' 'HR2' 'external' '100.0' '100.0' '100.0']['11/13/23 19:32:19' 'HR2' 'external' '100.0' '100.0' '100.0']"
        print("Received:", dataString)
        listof3 = dataString[1:-1].split("][")
        print("3list:",listof3)
        #allLists = ast.literal_eval()
        result = [x.split() for x in listof3]
        print(result)

        
        with open('output.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(result)

        # Send data back to the client
        # client_socket.send("Hello, client!".encode())
        break

except Exception as e:
    print(f"Error: {e}")

finally:
    client_socket.close()
    server_socket.close()
    print(f"Server socket closed.")
