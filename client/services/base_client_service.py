from PyQt6.QtCore import QObject, pyqtSignal


class BaseClientService(QObject):
    connection = pyqtSignal(bool)
    authorization = pyqtSignal(bool, int)
    message = pyqtSignal(object)
    public_key_received = pyqtSignal(str, int)
    def __init__(self):
        super().__init__()

    def connect(self, host: str, port: int):
        raise NotImplementedError()

    def _on_connected(self, con: bool):
        raise NotImplementedError()

    def authorize(self, name: str, email: str) -> None:
        raise NotImplementedError()

    def send_message(self, message: str, recipient_id: int, sender_name: str, encryption: str, encryption_key: str):
        raise NotImplementedError()

    def _on_message_recive(self, server_answer: str | bool) -> None:
        raise NotImplementedError()

    def request_public_key(self, recipient_id: int) -> None:
        raise NotImplementedError()