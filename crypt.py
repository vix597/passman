import struct
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

class FileCryptoTool:
    IV_SIZE = 16
    
    def __init__(self):
        pass
        
    def encrypt_file(password, path, file_data):
        key = SHA256.new(password.encode('utf-8')).digest()
        iv = Random.new().read(FileCryptoTool.IV_SIZE)
        encryptor = AES.new(key, AES.MODE_CFB, iv)
        
        with open(path,'wb') as out_file:
            out_file.write(iv + encryptor.encrypt(file_data))
        
    def decrypt_file(password, path):
        key = SHA256.new(password.encode('utf-8')).digest()
        
        with open(path,'rb') as in_file:
            iv = in_file.read(FileCryptoTool.IV_SIZE)
            decryptor = AES.new(key, AES.MODE_CFB, iv)
            return decryptor.decrypt(in_file.read())