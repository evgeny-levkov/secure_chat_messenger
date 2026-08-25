from PyQt6.QtCore import pyqtSignal, QObject
from ..services.base_client_service import BaseClientService
from ...common.models.message_model import MessageModel
from ..repositories.base_client_message_repository import BaseClientMessageRepository
from datetime import datetime


class ClientViewModel(QObject):
    connect_sign = pyqtSignal(bool)
    authorized = pyqtSignal(bool, int)
    message = pyqtSignal(datetime, int, str)
    def __init__(self, client_service: BaseClientService, db: BaseClientMessageRepository) -> None:
        super().__init__()
        self.client_service = client_service
        self.client_service.connection.connect(self._get_connection_res)
        self.client_service.authorization.connect(self._get_authorization_res)
        self.client_service.message.connect(self._get_send_message)
        self.db = db
        
    def connect(self, host: str, port: int) -> None:
        self.client_service.connect(host, port)

    def _get_connection_res(self, sig: bool) -> None:
        self.connect_sign.emit(sig)

    def authorization(self, name: str, email: str) -> None:
        self.client_service.authorize(name, email)

    def _get_authorization_res(self, sig: bool, user_id: int) -> None:
        self.my_id = user_id
        self.authorized.emit(sig, user_id)

    def send_message(self, message: str, recipient_id: int):
        self.client_service.send_message(message, recipient_id)
        time_now = datetime.now()
        self.db.save_message(MessageModel(message, time_now, self.my_id, recipient_id))
        self.message.emit(time_now, self.my_id, message)

    def _get_send_message(self, message: MessageModel) -> None:
        time = message.time
        sender = message.sender
        text_mes = message.message
        self.db.save_message(message)
        self.message.emit(time, sender, text_mes)

    def get_history(self, id_senders: int, id_recipient: int) -> list[MessageModel] | None:
        return self.db.get_history(id_senders, id_recipient)