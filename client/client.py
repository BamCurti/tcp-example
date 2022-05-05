import socket
import nacl.secret
import nacl.utils
from nacl.signing import SigningKey

class Client():
    buffer:bytes=None #Raw buffer
    encrypted_buffer: bytes=None #Buffer to be sent
    
    def __init__(self, port=4040, hostname='localhost'):
        self.get_aes_key()
        
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self.hostname = 'localhost'
        self.port = 4040
        
        server_address = (hostname, port)
        print('connecting to {} port {}'.format(*server_address))
        self.sock.connect(server_address)  
        
    def get_aes_key(self):
        with open('server/secret.bin', 'rb') as f:
            self.key = f.read()
        
    def encrypt(self, buffer):
        #first, encrypt it
        box = nacl.secret.SecretBox(self.key)
        
        #last, lets sign it
        return self.signing_key.sign(box.encrypt(buffer))
            
    def send_file(self, filename):
        try:
            f = open(filename, 'rb')
            l = f.read(1024)
            print('Sending...')
            
            while l:
                l = self.encrypt(l)
                self.sock.send(l)
                l = f.read(1024)
                    
        except Exception as e:
            print(e)

        finally:
            f.close()
            self.sock.close()
            print('File sent!')

    def sign(self):
        #Generate a new random signing key
        self.signing_key = SigningKey.generate()
        verify_key = self.signing_key.verify_key
        
        with open('sign.bin', 'wb') as f:
            f.write(verify_key.encode())
            
        print('Sign generated!')