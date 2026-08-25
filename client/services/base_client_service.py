from abc import ABC, abstractmethod
from PyQt6.QtCore import QObject, pyqtSignal


class BaseClientService(QObject, ABC):
    connection = pyqtSignal(bool)
    authorization = pyqtSignal(bool, int)
    message = pyqtSignal(object)
    @abstractmethod
    def connect(self, host: str, port: int):
        pass

    @abstractmethod
    def _on_connected(self, con: bool):
        pass

    @abstractmethod
    def authorize(self, name: str, email: str) -> None:
        pass

    @abstractmethod
    def send_message(self, message: str, recipient_id: int):
        pass

    @abstractmethod
    def _on_message_recive(self, server_answer: str | bool) -> None:
        pass