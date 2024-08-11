import threading
from server import start_server
from GUI import root

def run_server():
    print("Starting server...")
    start_server()

if __name__ == "__main__":
    run_server()
