import socket
import threading
from colorama import init, Fore

init(autoreset=True)

# Choose a Nickname
chosen_nickname = input("Choose your nickname: ")

# Connect To Server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 55555))

# Listen to Server and Send Nickname
def receive_messages():
    while True:
        try:
            # Send Nickname to Server
            message = client_socket.recv(1024).decode('ascii')
            if message == 'NICK':
                client_socket.send(chosen_nickname.encode('ascii'))
            else:
                print(Fore.GREEN + message)
        except:
            # Close Connection On Error
            print(Fore.RED + "An error occurred, TCP-server is down!")
            client_socket.close()
            break
            
# Send Messages To Server
def send_messages():
    while True:
        message = '{}: {}'.format(chosen_nickname, input(''))
        client_socket.send(message.encode('ascii'))
        
# Start Threads For Listening And Writing
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

write_thread = threading.Thread(target=send_messages)
write_thread.start()
