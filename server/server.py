import socket
    
class Server():
    def __init__(self, port=4040, hostname='localhost'):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #bind the socket to the port
        server_address = (hostname, port)
        
        print('Running the server on http://{}:{}'.format(*server_address))
        self.sock.bind(server_address)
        
        # Listen for incoming connections
        self.sock.listen(1)
        
    def get_aes_key(self):
        pass
        
    def decrypt(self, buffer):
        pass
        
    def run(self, path):
        while True:
            connection, client_address = self.sock.accept()
            try:
                f = open(path, 'wb')
                print(f'Connection from {client_address}')
                
                # Receive the data in small chunks                
                while True:
                    data = connection.recv(1024)
                    f.write(data)
                    
                    if not data:
                        print(f'No data from {client_address}')
                        break
                    
            except Exception as e:
                f.close()
                print(e)
                
            finally:
                connection.close()