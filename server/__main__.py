from server import Server

def main():
    #sock = server.create()
    #server.run(sock, 'server/file.txt')
    
    sock = Server()
    input('Click enter to read the sign...')
    sock.read_sign()
    input('Click enter to receive the file...')
    sock.run('server/file.txt')
    
if __name__ == '__main__':
    main()