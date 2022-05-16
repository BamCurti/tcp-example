#String declaration
from typing import Union

#login
import logging

#encrypting
import nacl.secret
import nacl.utils

#Signing
from nacl.signing import VerifyKey
from nacl.signing import SigningKey


class SecurityManager():
    key: bytes
    
    def __init__(self):
        #Logging needs configuration
        logging.basicConfig(filename='info.log', format='%(asctime)s - %(message)s', level=logging.INFO)
        self.key = None
        self.sign = None
        self.verify_key = None
    
    def separate_name(self, dir, extension, sufix=''):
        #Separate the name of the file and the extension, so we can use the name in the encrypt file.
        name_list = dir.rsplit('.')
        return f'{name_list[0]}{sufix}.{extension}'
    
    def log(self, msg: str):
        """Log every operation done.

        Args:
            msg (str): An message to be appended to the log file.
        """
        logging.info(msg)

    def generate_key(self, dirname: str):
        """Generate a random key for encrypting operations. The key will be saved in a file defined by the user.

        Args:
            dirname (str, optional): The dirname of the file to generate the key. Defaults to 'key.bin'.
        """
        self.log(f'Key generated')
        
        #First, we generate a random key to be saved on a local file and as attribute
        key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
        self.key = key
        
        self.write_file('key.bin', key, 'wb')
            
    def read_key(self, dirname='key.bin'):
        """Read an existing key from a directory.

        Args:
            dirname (str, optional): The directory to read the key from. Defaults to 'key.bin'.
        """ 
        self.key = self.read_key(dirname, mode='rb')
            
        self.log(f'Key read from {dirname}')

    def read_file(self, dir: str, mode='r'):
        """Read an existing file from a directory, in order to encrypt or decrypt it.

        Args:
            dir (str): The directory of the file to read.
            mode (str, optional): the mode to be read. Defaults to 'r'.

        Returns:
            bytes: The file as bytes, in order to encrypt.
        """
        info = None
        with open(dir, mode=mode) as f:
            info = f.read()
            
        self.log(f'Read file from {dir}')
        return info
    
    def write_file(self, dir: str, buf: Union[bytes ,str], mode='w'):
        with open(dir, mode=mode) as f:
            f.write(buf)
            
        self.log(f'File written to {dir}')
            
    def encrypt_file(self, dir: str, key_dir: str='key.bin'):
        """Encrypt a file using NaCl features. If there is no key provided, it will create a new one.

        Args:
            dir (str): The file to encrypt.
        """
        
        if self.key is None:
            self.generate_key(key_dir)

        #Separate the name of the file and the extension, so we can use the name in the encrypt file.
        nameList = dir.rsplit('.')
        name = nameList[0]

        #Next, lets create the box to encrypt the file
        box = nacl.secret.SecretBox(self.key)
        
        #The buffer to encrypt
        buffer = self.read_file(dir, 'rb')
        encrypt_buffer = box.encrypt(buffer)
        
        self.write_file(f'{name}.bin', encrypt_buffer, 'wb')
        
        self.log(f'File encypted: {name}.bin')
        
    def decrypt_file(self, dir: str, key_dir: str='key.bin', extension='txt'):
        if self.key is None:
            self.read_key(key_dir)
            
        #Separate the name of the file and the extension, so we can use the name in the encrypt file.
        nameList = dir.rsplit('.')
        name = nameList[0]
        
        #Next, lets create the box to encrypt the file
        box = nacl.secret.SecretBox(self.key)
        
        buffer = self.read_file(dir, 'rb')
        decrypt = box.decrypt(buffer)
        
        decrypt_dir = f'{name}.decrypt.{extension}'
        
        self.write_file(decrypt_dir, decrypt, 'wb')
        self.log(f'File decrypted successfully: {decrypt_dir}')
        
    def create_signature(self, dir):
        self.signing_key = SigningKey.generate()
        verify_key = self.signing_key.verify_key
        
        self.sign = verify_key.encode()
        
        self.write_file(dir, self.sign, 'wb')
        
        self.log(f'Signing key generated: {dir}')
        
    def sign_file(self, dir: str, sign_dir='sign.bin'):
        if self.sign is None:
            self.create_signature(dir=sign_dir)
            
        buf = self.read_file(dir, mode='rb')
        signed = self.signing_key.sign(buf)
        name = self.separate_name(dir, 'bin', '.signed')
        
        self.write_file(name, signed, 'wb')
        
        self.log(f'File {dir} signed: {name}')
        
    def read_signature(self, dir: str): 
        self.sign = self.read_file(dir, mode='rb')
        self.verify_key = VerifyKey(self.sign)
        
        self.log(f'Sign read from {dir}')
        
    def verify_signature(self, dir: str, sign_dir: str = 'sign.bin'):
        if self.verify_key is None:
            self.read_signature(sign_dir)
        
        buf = self.read_file(dir, 'rb')
        verify = self.verify_key.verify(buf)
        name = self.separate_name(dir, 'txt', '.verified')
        
        self.write_file(name, verify, 'wb')
        
        
        self.log(f'File verified: {dir}')