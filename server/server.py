import socket
    
def create():
    # Create the TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #bind the socket to the port
    port = 4040
    hostname = 'localhost'
    
    server_address = (hostname, port)
    print('Running the server on http://{}:{}'.format(*server_address))
    sock.bind(server_address)
    
    # Listen for incoming connections
    sock.listen(1)
    return sock
    
def run(sock, path):
    while True:
        connection, client_address = sock.accept()
        
        with open(path, 'wb') as f:        
            try:
                print(f'Connection from {client_address}')
                
                # Receive the data in small chunks and retrasmit it
                while True:
                    data = connection.recv(1024)
                    f.write(data)
                    
                    if not data:
                        print(f'No data from {client_address}')
                        break
                
            finally:
                connection.close()