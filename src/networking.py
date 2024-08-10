# src/networking.py
import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("Server started on port 12345")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address}")
        client_socket.send(b"Welcome to the server!")
        client_socket.close()

if __name__ == "__main__":
    start_server()
