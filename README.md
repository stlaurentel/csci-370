# Bluetooth Communication Setup

This repository demonstrates a simple Bluetooth communication setup between a server (your computer) and a client (Raspberry Pi). The instructions below guide you through the setup process on different operating systems.

## Cloning the Repository

Before running the server and client scripts, you need to clone the repository to your local machine or Raspberry Pi.

```bash
git clone https://github.com/stlaurentel/csci-370.git
cd csci-370
```

## Linux OS

On Linux-based operating systems (such as on the Raspberry Pi), you'll need to install the `python3-bluez` package to enable Bluetooth communication. Open a terminal and run the following command:

```bash
sudo apt install python3-bluez
```

## Windows OS

On Windows, you'll need to install PyBluez using pip. Run the following command to install PyBluez from the official repository:

```bash
pip install git+https://github.com/pybluez/pybluez.git#egg=pybluez
```

## Running the Server

1. Navigate to the "server" directory in this repository on your server or computer.

2. Run the following command to start the server:

```bash
python3 server.py
```
The server will start listening for a Bluetooth connection on a specific port.

Once you see the message "Waiting for a Bluetooth connection on port X" (where X is the port number), the server is ready to accept connections.

## Running the Client (Raspberry Pi)

1. Navigate to the "client" directory on your Raspberry Pi.

2. Run the following command to start the client, replacing {port} with the actual port number displayed on the server:

```bash
python3 client.py {port}
```
The client will attempt to connect to the server over Bluetooth.

If the connection is successful, you will be able to see the message "Hello, server!!!" received by the server end.
