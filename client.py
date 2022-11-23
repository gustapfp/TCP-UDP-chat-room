import socket
import threading

# Define the length of the message 
HEADER = 1024
# Define the format of the message 
FORMAT = 'utf-8'
# Define the port we're runing the server
PORT = 5050
# Get local IPv4 adress 
SERVER = socket.gethostbyname(socket.gethostname())
# Bind to a adress
ADDR = (SERVER, PORT)
# Disconectiong message to notify the server
DISCONECT_MESSAGE = ">DISCONECT<"

# Client username

username = input("Choose a username: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting to the server
client.connect(ADDR)

# def send_msg(msg):
#     """ Send messages to the server

#     Args:
#         msg (str): message to the server
#     """
#     message = msg.encode(FORMAT) # Encode the string into byte object
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT) # Encode msg_length into string
    
#     # Pad to make this length 64 
#     send_length += b' ' * (HEADER - len(send_length)) # Get the length of the message and subtract from the header
#     client.send(send_length)
#     client.send(message)
#     print(client.recv(HEADER).decode(FORMAT))

def client_recive():
    while True:
        try:
            message = client.recv(HEADER).decode(FORMAT)
            if message == "Username?":
                # client.send_msg(message)
                client.send(username.encode(FORMAT))
            else:
                print(message) 
        except:
            print('[->ERROR<-]')
            client.close()
            break

def client_send():
    while True:
        user_msg = f"{username}: {input('->')}"
        client.send(user_msg.encode(FORMAT))

       
        #client.send(user_msg.encode(FORMAT))



recive_theread = threading.Thread(target=client_recive)
recive_theread.start()

send_theread = threading.Thread(target=client_send)
send_theread.start()

