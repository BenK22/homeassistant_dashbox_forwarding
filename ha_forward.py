import socket
import select
import sys
'''Replace "thread" with "_thread" for python 3'''
from thread import *

# Replace with HA server ip and any port
server_address = '192.168.2.96'
server_port = 5001

# Replace with DashBox IP and 8001 or 8002
dashbox_ip = '192.168.2.96'
dashbox_port = 8002

# Replace with HA server ip and port the GEM config is listening on
ha_ip = '192.168.2.31'
ha_port = 8002

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((server_address, server_port))

ha = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ha.connect((ha_ip, ha_port))

# remove comment for debugging
#ha.sendall('Connected to HA.')

server.listen(100)
 
list_of_clients = [ha]

def clientthread(conn):
 
    # sends a message to the client whose user object is conn
    conn.send("Welcome to this chatroom!")
 
    while True:
            try:
                message = conn.recv(2048)
                if message:
 
                    # remove comment for debugging
                    #print (message)
 
                    # Calls broadcast function to send message to all
                    broadcast(message, conn)

                    # remove comment for debugging
                    #print 'Sending to DashBox'
                    dashbox = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    dashbox.connect((dashbox_ip, dashbox_port))
                    dashbox.sendall(message)
                    dashbox.close()
 
                else:
                    """message may have no content if the connection
                    is broken, in this case we remove the connection"""
                    remove(conn)
 
            except:
                continue
 
"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """
def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)
 
"""The following function simply removes the object
from the list that was created at the beginning of
the program"""
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


start_new_thread(clientthread, (ha,))

while True:
 
    """Accepts a connection request and stores two parameters,
    conn which is a socket object for that user, and addr
    which contains the IP address of the client that just
    connected"""
    conn, addr = server.accept()
 
    """Maintains a list of clients for ease of broadcasting
    a message to all available people in the chatroom"""
    list_of_clients.append(conn)
 
    # remove comment for debugging
    #print (addr[0] + " connected")
 
    # creates and individual thread for every user
    # that connects
    start_new_thread(clientthread,(conn,))
 
conn.close()
server.close()