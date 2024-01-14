import socket
import threading
from colorama import init, Fore

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

# Sending Messages To All Connected Clients
def broadcast(message, client_sender):
    for client in clients:
        if client != client_sender:
            client.send(message)

# Function to remove a client
def remove(client):
    if client in clients:
        index = clients.index(client)
        nickname = nicknames[index]
        broadcast((Fore.RED + '{} left the chat room.'.format(nickname)).encode('ascii'), client)
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
            broadcast(message, client)
        except:
            # Removing And Closing Clients
            remove(client)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(Fore.GREEN + "Connected with {}".format(str(address)))

        # Request And Store Nicknames
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print(Fore.GREEN + "Nickname: {}".format(nickname))
        broadcast((Fore.GREEN + "{} joined the chat room.".format(nickname)).encode('ascii'), client)
        client.send('Connected to server. Start chatting!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Start receiving function
receive()

