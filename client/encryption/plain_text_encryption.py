from .encryption_factory import EncryptionFactory
from .base_encryption import BaseEncryption


@EncryptionFactory.register_encryption('Без шифрования')
class PlainTextEncryption(BaseEncryption):
    def __init__(self, key=None) -> None:
        self.key = key

    def encryption(self, text: str) -> str:
        return text

    def decryption(self, text: str) -> str:
        return text