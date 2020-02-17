import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)
            print('received "%s"' % data)
            if data:
                lst = data.decode().split(' ')
                lst = [int(x) for x in lst]
                response = str.encode(str(sum(lst)) +' '+ str(sum(lst)/5) +' '+ str(max(lst)))
                connection.sendall(response)
                break
            else:
                break
                
            
    finally:
        # Clean up the connection
        connection.close()
