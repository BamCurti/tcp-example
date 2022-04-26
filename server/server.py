import socket
import nacl.secret
import nacl.utils

class Server():
    buffer: bytes = None
    encrypted_buffer : bytes = None
    key: str = None
    
    def __init__(self, port=4040, hostname='localhost'):
        self.get_aes_key()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #bind the socket to the port
        server_address = (hostname, port)
        
        print('Running the server on http://{}:{}'.format(*server_address))
        self.sock.bind(server_address)
        
        # Listen for incoming connections
        self.sock.listen(1)
        
    def get_aes_key(self):
        with open('server/secret.txt', 'rb') as f:
            self.key = f.read()
            
        
    def decrypt(self, buffer):
        box = nacl.secret.SecretBox(self.key)
        return box.decrypt(buffer)

    def run(self, path):
        while True:
            connection, client_address = self.sock.accept()
            try:
                f = open(path, 'wb')
                print(f'Connection from {client_address}')
                
                # Receive the data in small chunks                
                while True:
                    data = connection.recv(1024)
                    data = self.decrypt(data)
                    f.write(data)
                    print(data)
                    
                    if not data:
                        print(f'No data from {client_address}')
                        break
                    
            except Exception as e:
                f.close()
                print(e)
                
            finally:
                connection.close()