import socket
import os
import time  
from tkinter import simpledialog

# --> Automatic port allocation (for server and client then port number can be obtained as follows)

# server_socket.bind(("localhost", 0))

# # Get the port number that was chosen
# server_port = server_socket.getsockname()[1]

SERVER_PORT = 12345
BUFFER_SIZE = 1024

def connect_to_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect(("localhost", SERVER_PORT))
        return client_socket
    except ConnectionRefusedError:
        print("Failed to connect to the server.")
        return None




