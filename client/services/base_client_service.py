from PyQt6.QtCore import QObject, pyqtSignal


class BaseClientService(QObject):
    connection = pyqtSignal(bool)
    authorization = pyqtSignal(bool, int)
    message = pyqtSignal(object)
    def connect(self, host: str, port: int):
        raise NotImplementedError()

    def _on_connected(self, con: bool):
        raise NotImplementedError()

    def authorize(self, name: str, email: str) -> None:
        raise NotImplementedError()

    def send_message(self, message: str, recipient_id: int, sender_name: str, encryption: str):
        raise NotImplementedError()

    def _on_message_recive(self, server_answer: str | bool) -> None:
        raise NotImplementedError()