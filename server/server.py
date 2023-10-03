import bluetooth

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_socket.bind(("", bluetooth.PORT_ANY))    # Bind to any available port for RFCOMM
server_socket.listen(1)                         # Listen for one incoming connection

port = server_socket.getsockname()[1]           # Get the dynamically assigned port

print(f"Waiting for a Bluetooth connection on port {port}...")

client_socket, client_address = server_socket.accept()
print(f"Accepted connection from {client_address}")

# Receive data from the client
try:
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print("Received:", data.decode())

        # Send data back to the client
        # client_socket.send("Hello, client!".encode())
            # This function will trigger an error to be thrown:
            # Error: PY_SSIZE_T_CLEAN macro must be defined for '#' formats
            # This is an issue with pybluez. Need to find a way to fix
        break

except Exception as e:
    print(f"Error: {e}")

finally:
    client_socket.close()
    server_socket.close()
    print(f"Server socket closed.")