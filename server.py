import socket
import threading # to make sure that we're not blocking other clients


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

# Create a socket to connect this divice to other connections
local_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Define the kind of ip adress we're looking for

# Bound the adress to the socket "local_server"
local_server.bind(ADDR) 

# List of all the messages sended
msgs_stored = []

# list of clients

clients = []
 # clients usernames
usernames = []

print("[STARTING] your server is starting...")
print(f"[LISTENING] Server is listening on {SERVER}.")
local_server.listen() # Listening new conections


def broadcast(msg):
    """Send a message to all the users
    """
    for client in clients:
        client.send(msg)



def handle_client(conn, addr):
    """Handle all of the communication between the clients and the server

    Args:
        conn (_type_): connection
        addr (_type_): addres
    """
    print(f"[NEW CONNECTION] {addr} connect to the server.")

    connected = True
    while True:
        try:
            msg_length = conn.recv(HEADER) # Define how many bites we will recive from the client
            broadcast(msg) # send the message for everyone in the room
            if msg_length: # checking if the message isn't null or none
                msg_length = int(msg_length.decode(FORMAT)) # Decode from byte to UTF format
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONECT_MESSAGE:
                    connected = False
                print(f"[{addr}] send: {msg}")

                # Send a message to the client
                conn.send("[MESSAGE RECIVED] ...".encode(FORMAT))
        except:
            index = clients.index(conn)
            clients.remove(conn)
            conn.close()
            username = usernames[index]
            broadcast(f"[CHECKOUT] {username} has left the chat room.".encode(FORMAT))
            usernames.remove(username)
            connected = False
            
            
               
    
    conn.close()




def start(server):
    """ Start the socket server
    
    Args:
        server (_type_): server ip
    """
    
    while True: # The server will keep runing until the server is stopped or crashes

       # When a connection occurs the addres of the connection (and a object to send information to thant connection) are stored
       conn,  addr = server.accept()
       conn.send("Username?".encode(FORMAT))
       username = conn.recv(HEADER)
       usernames.append(username)
       clients.append(conn)
       print(f"[REGISTERED] The username of this user is: {username}.".encode(FORMAT))
       broadcast(f"[CHECKIN] {username.decode(FORMAT)} has connected to the chat room.".encode(FORMAT))
       conn.send(f"[CHECKIN] You are connected {username.decode(FORMAT)}!".encode(FORMAT))


       thread = threading.Thread(target=handle_client, args=(conn, addr))
       thread.start()

       # Print the amount of active connections in ther server
       print(f"[ACTIVE CONNECTIONS] {threading.active_count() -1}") # -1 because the listen connection doesn't count



if __name__ == "__main__":
    
    start(local_server)