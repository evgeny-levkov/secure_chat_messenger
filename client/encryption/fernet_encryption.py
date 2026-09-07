from cryptography.fernet import Fernet
from .base_encryption import BaseEncryption
from .encryption_factory import EncryptionFactory


@EncryptionFactory.register_encryption('Fernet')
class FernetEncryption(BaseEncryption):
    def __init__(self, key=None) -> None:
        self.key = key

    def generate_key(self) -> None:
        self.key = Fernet.generate_key()

    def encryption(self, text: str) -> str:
        cipher = Fernet(self.key)
        return cipher.encrypt(text.encode()).decode('utf-8')

    def decryption(self, text: str) -> str:
        cipher = Fernet(self.key)
        return cipher.decrypt(text.encode()).decode('utf-8')