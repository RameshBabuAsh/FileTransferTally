import socket
import threading
import os

# --> Automatic port allocation

# server_socket.bind(("localhost", 0))

# # Get the port number that was chosen
# server_port = server_socket.getsockname()[1]

SERVER_PORT = 12345
BUFFER_SIZE = 1024

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", SERVER_PORT))
    server_socket.listen(5)
    print("Server started, waiting for clients to connect...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client {client_address} connected.")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def handle_client(client_socket):
    try:
        # Receive the username
        username = receive_message(client_socket).strip()
        print(f"Username received: {username}")

        # Create a directory for the user if it doesn't exist
        user_directory = os.path.join("ALL_CLIENTS", username)
        if not os.path.exists(user_directory):
            os.makedirs(user_directory)

        while True:
            # Receive the filename
            filename = receive_message(client_socket).strip()
            if not filename:
                print("No filename received. Closing connection.")
                break

            # print(f"Filename received: {filename}")

            # Path to save the file
            file_path = os.path.join(user_directory, filename)
            with open(file_path, 'wb') as file:
                while True:
                    file_data = client_socket.recv(BUFFER_SIZE)
                    if not file_data:
                        break
                    file.write(file_data)

            print(f"File {filename} saved to {user_directory}. Admin sent successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def receive_message(client_socket):
    message = b""
    while True:
        part = client_socket.recv(BUFFER_SIZE)
        message += part
        if len(part) < BUFFER_SIZE:
            break
    return message.decode('utf-8')