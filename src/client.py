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

def send_file(client_socket, file_path, username):
    try:
        # Send the username to the server
        client_socket.send(username.encode('utf-8'))
        time.sleep(1)  # Adding delay

        # Send the filename to the server
        filename = os.path.basename(file_path)
        client_socket.send(filename.encode('utf-8'))
        time.sleep(1)  # Adding delay

        # Send the file content
        with open(file_path, 'rb') as file:
            while (data := file.read(BUFFER_SIZE)):
                client_socket.send(data)
        
        print("File sent successfully.")
    except Exception as e:
        print(f"Failed to send file: {e}")

def join_group(client_socket):
    group_name = simpledialog.askstring("Input", "Enter group name to join:")
    if group_name:
        message = f"JOIN {group_name}"
        client_socket.send(message.encode('utf-8'))
