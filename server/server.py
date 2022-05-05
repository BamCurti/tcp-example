import socket
import nacl.secret
import nacl.utils
from nacl.signing import VerifyKey

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
        with open('server/secret.bin', 'rb') as f:
            self.key = f.read()
            
    def read_sign(self):
        #Read the signing key generated from client
        with open('sign.bin', 'rb') as f:
            self.verify_key_bytes = f.read()
        print('Sign read!')
        
        self.verify_key = VerifyKey(self.verify_key_bytes)
        
    def decrypt(self, buffer):
        #first, lets designing
        buf = self.verify_key.verify(buffer)
        
        #then, decrypt
        box = nacl.secret.SecretBox(self.key)
        return box.decrypt(buf)

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