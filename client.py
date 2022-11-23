import socket
import select
import errno

# Define the length of the message 
HEADER = 64
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

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connecting to the server
client.connect(ADDR)


def send(msg):
    """ Send messages to the server

    Args:
        msg (str): message to the server
    """
    message = msg.encode(FORMAT) # Encode the string into byte object
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT) # Encode msg_length into string
    
    # Pad to make this length 64 
    send_length += b' ' * (HEADER - len(send_length)) # Get the length of the message and subtract from the header
    client.send(send_length)
    client.send(message)
    print(client.recv(HEADER).decode(FORMAT))

if __name__ == '__main__': 
    while True:
        user_msg = input()
        if user_msg is DISCONECT_MESSAGE:
            
            False
        send(user_msg)
