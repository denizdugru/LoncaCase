from cryptography.fernet import Fernet


class Cipher:
    def __init__(self, key):
        self.key = key
        self.cipher_suite = Fernet(self.key)

    def encrypt(self, text):
        encrypted_text = self.cipher_suite.encrypt(text.encode())
        return encrypted_text

    def decrypt(self, encrypted_text):
        decrypted_text = self.cipher_suite.decrypt(encrypted_text).decode()
        return decrypted_text
