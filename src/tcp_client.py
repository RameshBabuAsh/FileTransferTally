import socket

# Client configuration
SERVER_HOST = '192.168.1.100'  # Replace with the server's IP address
SERVER_PORT = 12345
BROADCAST_PORT = 12346
BUFFER_SIZE = 1024
DISCOVERY_MESSAGE = "DISCOVER_GROUPS"

# Discover available groups
def discover_groups():
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_socket.sendto(DISCOVERY_MESSAGE.encode('utf-8'), ('<broadcast>', BROADCAST_PORT))
    
    print("[*] Sent discovery broadcast")

    broadcast_socket.settimeout(5)
    try:
        data, server_address = broadcast_socket.recvfrom(BUFFER_SIZE)
        groups = data.decode('utf-8').split(',')
        print(f"[*] Available groups: {groups}")
        return groups
    except socket.timeout:
        print("[-] No groups found")
        return []

# Join a group and receive files
def join_group(group_name):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))
    client.send(group_name.encode('utf-8'))
    print(f"[*] Joined {group_name}")

    while True:
        try:
            data = client.recv(BUFFER_SIZE)
            if not data:
                break
            with open(f"received_file_{group_name}.bin", 'wb') as f:
                f.write(data)
            print(f"[+] File received in {group_name}")
        except:
            print(f"[-] Failed to receive file in {group_name}")
            break
    
    client.close()
    print(f"[*] Disconnected from {group_name}")

if __name__ == "__main__":
    available_groups = discover_groups()
    if available_groups:
        group_name = input("Enter the group you want to join: ")
        if group_name in available_groups:
            join_group(group_name)
        else:
            print(f"[-] Invalid group: {group_name}")
