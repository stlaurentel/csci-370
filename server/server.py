#define PY_SSIZE_T_CLEAN 1
import bluetooth
import numpy as np
import ast
import re
import csv
import json


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
        print("datastring ",dataString)
        # dataString format: "['11/13/23-19:32:19' 'HR2' 'external' '100.0' '100.0' '100.0']['11/13/23 19:32:19' 'HR2' 'external' '100.0' '100.0' '100.0']['11/13/23 19:32:19' 'HR2' 'external' '100.0' '100.0' '100.0']"
        # Fix the format by adding commas between elements
        dataString = dataString.replace(" ", " , ")
        dataString = dataString.replace("\n", "")
        fixed_data_string = dataString.replace("']['", "'],['")
        fixed_data_string = fixed_data_string.replace(", ,",",")
        fixed_data_string = fixed_data_string.replace("-"," ")

        print("fixed datastr ",fixed_data_string)

        data_list = ast.literal_eval(f"[{fixed_data_string}]")

        csv_buffer = []

        # Convert each inner list to a CSV row
        for inner in data_list:
            csv_buffer.append([item.replace(', ,', '') for item in inner])

        # Write the CSV data to a file (or do anything else with it)
        with open('output.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(csv_buffer)
        print("done")

        break

except Exception as e:
    print(f"Error: {e}")

finally:
    client_socket.close()
    server_socket.close()
    print(f"Server socket closed.")
