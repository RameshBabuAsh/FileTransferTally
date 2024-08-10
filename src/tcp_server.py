import socket
import threading
import os

# Server configuration
HOST = '0.0.0.0'
PORT = 12345
BROADCAST_PORT = 12346
BUFFER_SIZE = 1024
DISCOVERY_MESSAGE = "DISCOVER_GROUPS"
LOG_FILE = 'log.txt'

# Groups data structure
groups = {
    'Group 1': [],
    'Group 2': [],
    'Group 3': []
}

# Write log
def write_log(message):
    with open(LOG_FILE, 'a') as f:
        f.write(message + "\n")
    print(message)

# Handle client connection
def handle_client(client_socket, address):
    group_name = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    if group_name in groups:
        groups[group_name].append(client_socket)
        write_log(f"[+] {address} joined {group_name}")
        try:
            while True:
                message = client_socket.recv(BUFFER_SIZE)
                if not message:
                    break
        except:
            pass
    else:
        write_log(f"[-] {address} attempted to join an invalid group")
    
    write_log(f"[-] {address} disconnected from {group_name}")
    client_socket.close()

# Handle discovery requests
def handle_discovery():
    discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    discovery_socket.bind((HOST, BROADCAST_PORT))
    print(f"[*] Listening for discovery on {HOST}:{BROADCAST_PORT}")
    
    while True:
        message, client_address = discovery_socket.recvfrom(BUFFER_SIZE)
        if message.decode('utf-8') == DISCOVERY_MESSAGE:
            available_groups = ",".join(groups.keys())
            discovery_socket.sendto(available_groups.encode('utf-8'), client_address)

# Send file to a group
def send_file_to_group(group_name, file_path):
    if group_name in groups:
        clients = groups[group_name]
        failed_clients = []
        with open(file_path, 'rb') as file:
            data = file.read()
            for client_socket in clients:
                try:
                    client_socket.sendall(data)
                    write_log(f"[+] File sent to client {client_socket.getpeername()} in {group_name}")
                except:
                    write_log(f"[-] Failed to send file to {client_socket.getpeername()} in {group_name}")
                    failed_clients.append(client_socket.getpeername())
        write_log(f"[*] File transfer complete to {group_name}. Failed clients: {failed_clients}")
    else:
        write_log(f"[-] Attempt to send file to invalid group {group_name}")

# Main server loop
def start_server():
    # Start discovery thread
    discovery_thread = threading.Thread(target=handle_discovery)
    discovery_thread.daemon = True
    discovery_thread.start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[*] Server listening on {HOST}:{PORT}")
    
    while True:
        client_socket, address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()

if __name__ == "__main__":
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()  # Create log file if it doesn't exist
    start_server()
