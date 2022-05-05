from client import Client

def main():
    
    sock = Client()
    sock.sign()
    input('Click enter to start sending the file...')
    sock.send_file('client/message.txt')
    
    #server = client.create_server()
    #client.send_file(server, 'client/message.txt')
    
if __name__ == '__main__':
    main()