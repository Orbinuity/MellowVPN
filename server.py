import socket
import requests
import threading

# Server configuration
SERVER_HOST = "10.22.12.60"  # Fixed server IP
SERVER_PORT = 12346
clients = {}  # Dictionary to store connected clients { (ip, port): socket }

def find_command(command):
    if command[0] == 'get':
        if command[1] == 'site':
            response = requests.get(command[2])

            if response.status_code == 200:
                html_code = str(response.text)
                return html_code
            else:
                return f"Failed to retrieve the page. Status code: {response.status_code}"
        else:
            return "Invalid command!"
    else:
        return "Invalid command!"

# Handle client communication
def handle_client(client_socket, address):
    print(f"[*] New connection from {address[0]}:{address[1]}")
    clients[address] = client_socket

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Message from {address[0]}:{address[1]}: {message}")

            send_messages(address[0], address[1], find_command(eval(message)))
        except ConnectionResetError:
            break

    print(f"[*] Connection closed for {address[0]}:{address[1]}")
    del clients[address]
    client_socket.close()

# Function to send messages to specific clients
def send_messages(ip, port, message):
    if not clients:
        print("[*] No connected clients.")

    try:
        target_addr = (str(ip), int(port))

        if target_addr in clients:
            clients[target_addr].sendall(message.encode())
        else:
            print("[!] Invalid client. Try again.")

    except ValueError:
        print("[!] Invalid input. Enter valid IP and Port.")

# Start server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)  # Allow up to 5 clients
print(f"[*] Server listening on {SERVER_HOST}:{SERVER_PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
