import client

def main():
    
    sock = client.Client()
    sock.send_file('client/message.txt')
    
    #server = client.create_server()
    #client.send_file(server, 'client/message.txt')
    
if __name__ == '__main__':
    main()