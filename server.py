import socket
import threading # to make sure that we're not blocking other clients


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
DISCONECT_NESSAGE = "->DISCONECT<-"

# Create a socket to connect this divice to other connections
local_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Define the kind of ip adress we're looking for

# Bound the adress to the socket "local_server"
local_server.bind(ADDR) 

def handle_client(conn, addr):
    """Handle all of the communication between the clients and the server

    Args:
        conn (_type_): connection
        addr (_type_): addres
    """
    print(f"[NEW CONNECTION] {addr} connect to the server.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER) # Define how many bites we will recive from the client
        msg_length = int(msg_length.decode(FORMAT)) # Decode from byte to UTF format
        msg = conn.recv(msg_length).decode(FORMAT)
        if msg == DISCONECT_NESSAGE:
            connected = False
        print(f"[{addr}] send: {msg}")
    
    conn.close()




def start(server):
    """ Start the socket server
    
    Args:
        server (_type_): server ip
    """
    print("[STARTING] your server is starting...")
    print(f'[LISTENING] Server is listening on {SERVER}')
    
    server.listen() # Listening new conections

    while True: # The server will keep runing until the server is stopped or crashes

       # When a connection occurs the addres of the connection (and a object to send information to thant connection) are stored
       conn,  addr = server.accept()
       thread = threading.Thread(target=handle_client, args=(conn, addr))
       thread.start()

       # Print the amount of active connections in ther server
       print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}") # -1 because the listen connection doesn't count

start(local_server)