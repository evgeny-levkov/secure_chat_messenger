from PyQt6.QtCore import QObject, pyqtSignal


class BaseClientService(QObject):
    connection = pyqtSignal(bool)
    authorization = pyqtSignal(bool, int)
    message = pyqtSignal(object)
    public_key_received = pyqtSignal(str, int)
    deleted = pyqtSignal(str)
    edited = pyqtSignal(str, str)
    founded_user = pyqtSignal(int, str)
    not_founded_user = pyqtSignal(str)
    def __init__(self) -> None:
        super().__init__()

    def connect(self, host: str, port: int) -> None:
        raise NotImplementedError()

    def _on_connected(self, con: bool) -> None:
        raise NotImplementedError()

    def authorize(self, name: str, email: str) -> None:
        raise NotImplementedError()

    def send_message(self, uuid: str, message: str, recipient_id: int, sender_name: str, encryption: str, encryption_key: str) -> None:
        raise NotImplementedError()

    def _on_message_recive(self, server_answer: str | bool) -> None:
        raise NotImplementedError()

    def request_public_key(self, recipient_id: int) -> None:
        raise NotImplementedError()

    def send_delete_message(self, uuid: str, recipient_id: int) -> None:
        raise NotImplementedError()

    def send_edit_message(self, uuid: str, recipient_id: int, message: str) -> None:
        raise NotImplementedError()

    def found_user(self, id: int) -> None:
        raise NotImplementedError()