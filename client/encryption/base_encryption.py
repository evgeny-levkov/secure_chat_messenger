from abc import ABC, abstractmethod


class BaseEncryption(ABC):
    def __init__(self, key=None) -> None:
        self.key = key
        
    @abstractmethod
    def encryption(self, text: str) -> str:
        pass

    @abstractmethod
    def generate_key(self) -> None:
        pass
    @abstractmethod
    def decryption(self, text: str) -> str:
        pass