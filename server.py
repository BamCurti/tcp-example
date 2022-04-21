import socket
import sys

def main():
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
    
    run(sock)
    
def run(sock):
    while True:
        connection, client_address = sock.accept()
        try:
            print(f'Connection from {client_address}')
            
            # Receive the data in small chunks and retrasmit it
            while True:
                data = connection.recv(16)
                print('Received {!r}'.format(data))
                
                if data:
                    print('Sending data back to the client')
                    connection.sendall(data)
                else:
                    print(f'No data from {client_address}')
                    break
            
        finally:
            connection.close()

if __name__ == '__main__':
    main()