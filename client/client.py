import socket

def create_server():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    hostname = 'localhost'
    port = 4040
    
    server_address = (hostname, port)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
    return sock
        
def send_message(sock):    
    try:
        # Send data
        message = b'This is the message.  It will be repeated.'
        print('sending {!r}'.format(message))
        sock.sendall(message)

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print('received {!r}'.format(data))

    finally:
        print('closing socket')
        sock.close()    
        
def send_file(sock, filename):
    try:
        with open(filename, 'rb') as f:
            l = f.read(1024)
            while l:
                print('Sending...')
                sock.send(l)
                l = f.read(1024)
                
    except Exception as e:
        print(f'Error sending {filename}')
        print(e)
            
    finally:
        print('closing socket')
        sock.close()         
