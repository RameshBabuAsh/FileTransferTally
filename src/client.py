import socket
import os
import time  
from tkinter import simpledialog

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




