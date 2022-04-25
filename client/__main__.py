import client

def main():
    
    server = client.create_server()
    client.send_file(server, 'client/message.txt')
    
if __name__ == '__main__':
    main()