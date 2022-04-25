import server

def main():
    #sock = server.create()
    #server.run(sock, 'server/file.txt')
    
    sock = server.Server()
    sock.run('server/file.txt')
    
if __name__ == '__main__':
    main()