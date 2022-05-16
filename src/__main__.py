from security import SecurityManager

def main():
    security_manager = SecurityManager()
    security_manager.encrypt_file('test.txt')
    security_manager.decrypt_file('test.bin')
    security_manager.sign_file('test.txt')
    security_manager.verify_signature('test.signed.bin')

if __name__ == '__main__':
    main()