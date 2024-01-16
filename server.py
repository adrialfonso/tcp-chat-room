import socket
import threading
from colorama import init, Fore, Style

init(autoreset=True)

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
colors = [Fore.RED + Style.BRIGHT, Fore.YELLOW + Style.BRIGHT, Fore.BLUE + Style.BRIGHT,
          Fore.MAGENTA + Style.BRIGHT, Fore.CYAN + Style.BRIGHT, Fore.WHITE + Style.BRIGHT,
          Fore.GREEN + Style.BRIGHT, Fore.LIGHTRED_EX + Style.BRIGHT, Fore.LIGHTYELLOW_EX + Style.BRIGHT, 
          Fore.LIGHTBLUE_EX + Style.BRIGHT, Fore.LIGHTMAGENTA_EX + Style.BRIGHT, Fore.LIGHTCYAN_EX + Style.BRIGHT, 
          Fore.LIGHTWHITE_EX + Style.BRIGHT]

# Add more colors if needed
client_colors = {}  # Dictionary to store client colors

print(Style.BRIGHT + Fore.GREEN + "TCP-Chat server listening...")

# Sending Messages To All Connected Clients
def broadcast(message, client_sender):
    sender_index = clients.index(client_sender)
    sender_color = client_colors[client_sender]
    
    for client, color in zip(clients, colors):
        if client != client_sender:
            client.send((sender_color + message).encode('ascii'))

# Function to remove a client
def remove(client):
    if client in clients:
        index = clients.index(client)
        nickname = nicknames[index]
        broadcast('{} left the chat room.'.format(nickname), client)
        nicknames.remove(nickname)
        clients.remove(client)
        client.close()
        print(Fore.RED + "{} left the chat room.".format(nickname))

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            if not message:
                remove(client)
                break
            broadcast(message.decode('ascii'), client)
        except:
            # Removing And Closing Clients
            remove(client)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(Style.BRIGHT + Fore.GREEN + "Connected with {}".format(str(address)))

        # Request And Store Nicknames
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)

        # Assign Color to Client
        client_color = colors[len(nicknames) - 1]  # Assign color based on order of connection
        client_colors[client] = client_color

        clients.append(client)

        # Print And Broadcast Nickname
        print(client_color + "Nickname: {}".format(nickname))
        broadcast("{} joined the chat room.".format(nickname), client)
        client.send('Connected to server. Start chatting!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Start receiving function
receive()
