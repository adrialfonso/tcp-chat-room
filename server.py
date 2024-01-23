import socket
import threading
from colorama import init, Fore, Style
import random

init(autoreset=True)

# Server Configuration
host = '127.0.0.1'
port = 55555

# Initialize Server
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind((host, port))
tcp_server.listen()

connected_clients = []
client_nicknames = []
available_colors = [Fore.RED + Style.BRIGHT, Fore.YELLOW + Style.BRIGHT, Fore.BLUE + Style.BRIGHT,
                    Fore.MAGENTA + Style.BRIGHT, Fore.CYAN + Style.BRIGHT, Fore.WHITE + Style.BRIGHT,
                    Fore.GREEN + Style.BRIGHT]
client_colors = {}

print(Style.BRIGHT + Fore.GREEN + "TCP-Chat server listening...")

# Send Messages To All Connected Clients
def send_message_to_all(message, sender_client):
    sender_index = connected_clients.index(sender_client)
    sender_color = client_colors[sender_client]
    
    for client, color in zip(connected_clients, available_colors):
        if client != sender_client:
            client.send((sender_color + message).encode('ascii'))

# Function to disconnect a client
def disconnect_client(client):
    if client in connected_clients:
        index = connected_clients.index(client)
        nickname = client_nicknames[index]
        send_message_to_all('{} left the chat room.'.format(nickname), client)
        client_nicknames.remove(nickname)
        connected_clients.remove(client)
        client.close()
        print(Fore.RED + "{} left the chat room.".format(nickname))

# Handle Messages From Clients
def handle_client_messages(client):
    while True:
        try:
            # Broadcast Messages
            message = client.recv(1024)
            if not message:
                disconnect_client(client)
                break
            send_message_to_all(message.decode('ascii'), client)
        except:
            # Disconnect Clients
            disconnect_client(client)
            break

# Receive Function
def start_server():
    while True:
        # Accept Connection
        client, address = tcp_server.accept()
        print(Style.BRIGHT + Fore.GREEN + "Connected with {}".format(str(address)))

        # Request And Store Nicknames
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        client_nicknames.append(nickname)

        # Assign Color to Client
        client_color = random.choice(available_colors)
        client_colors[client] = client_color

        connected_clients.append(client)

        # Print And Broadcast Nickname
        print(client_color + "Nickname: {}".format(nickname))
        send_message_to_all("{} joined the chat room.".format(nickname), client)
        client.send('Connected to server. Start chatting!'.encode('ascii'))

        # Start Thread For Client
        client_thread = threading.Thread(target=handle_client_messages, args=(client,))
        client_thread.start()

# Start the server
start_server()
