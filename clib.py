import socket
import threading

# Server connection details
SERVER_HOST = "10.22.12.60"  # Fixed server IP
SERVER_PORT = 12346

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))
client_ip, client_port = client_socket.getsockname()
print(f"[*] Connected to server at {SERVER_HOST}:{SERVER_PORT}")
print(f"[*] Your address: {client_ip}:{client_port}")

# Sending messages to the server
while True:
    msg = input("You (to Server): ")
    if msg.lower() == "exit":
        break
    client_socket.sendall(msg.encode())
    try:
        message = client_socket.recv(1024).decode()
        if not message:
            break
        print("[SERVER]:", message)
    except ConnectionResetError:
        print("[*] Connection lost.")
        break

# Close the client socket
client_socket.close()
