import socket

class Client():
    def __init__(self, port=4040, hostname='localhost'):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        self.hostname = 'localhost'
        self.port = 4040
        
        server_address = (hostname, port)
        print('connecting to {} port {}'.format(*server_address))
        self.sock.connect(server_address)  
        
    def get_aes_key(self):
        pass
        
    def decrypt(self, buffer):
        pass
        
    def send_file(self, filename):
        try:
            f = open(filename, 'rb')
            l = f.read(1024)
            while l:
                print('Sending...')
                self.sock.send(l)
                l = f.read(1024)
                    
        except Exception as e:
            print(f'Error sending {filename}')

        finally:
            f.close()
            self.sock.close()
            print('File sent!')

