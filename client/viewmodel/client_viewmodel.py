from PyQt6.QtCore import pyqtSignal, QObject
from ..services.base_client_service import BaseClientService
from common.models.message_model import MessageModel
from ..repositories.base_client_message_repository import BaseClientMessageRepository
from ..encryption.encryption_factory import EncryptionFactory
from ..encryption.base_encryption import BaseEncryption
from datetime import datetime


class ClientViewModel(QObject):
    connect_sign = pyqtSignal(bool)
    authorized = pyqtSignal(bool, int)
    message = pyqtSignal(datetime, int, str, str, str)
    def __init__(self, client_service: BaseClientService, db: BaseClientMessageRepository) -> None:
        super().__init__()
        self.client_service = client_service
        self.client_service.connection.connect(self._get_connection_res)
        self.client_service.authorization.connect(self._get_authorization_res)
        self.client_service.message.connect(self._get_send_message)
        self.db = db
        self.encrytion_key = None
        
    def connect(self, host: str, port: int) -> None:
        self.client_service.connect(host, port)

    def _get_connection_res(self, sig: bool) -> None:
        self.connect_sign.emit(sig)

    def authorization(self, name: str, email: str) -> None:
        self.my_name = name
        self.client_service.authorize(name, email)

    def _get_authorization_res(self, sig: bool, user_id: int) -> None:
        self.my_id = user_id
        self.authorized.emit(sig, user_id)

    def send_message(self, message: str, recipient_id: int, sender_name: str, encryption: str):
        time_now = datetime.now()
        if self.encrytion_key is None:
            self.fernet: BaseEncryption = EncryptionFactory.get_class(encryption)
            self.fernet.generate_key()
            new_message = self.fernet.encryption(message)
            self.db.save_message(MessageModel(new_message, time_now, self.my_id, sender_name, recipient_id, encryption))
            self.message.emit(time_now, self.my_id, sender_name, new_message)
        else:
            new_message = self.fernet.encryption(message)
            self.db.save_message(MessageModel(new_message, time_now, self.my_id, sender_name, recipient_id, encryption))
            self.message.emit(time_now, self.my_id, sender_name, new_message, encryption)
        self.client_service.send_message(new_message, recipient_id, sender_name, encryption)
        self.sender_name = sender_name
        
    def _get_send_message(self, message: MessageModel) -> None:
        time = message.time
        sender = message.sender
        encryption = message.encryption
        if self.encrytion_key is None:
            self.fernet: BaseEncryption = EncryptionFactory.get_class(encryption)
            self.fernet.key = ТУТ ВООБЩЕ ВСЁ МЕНЯЕТСЯ МЫ ЖЕ ПЕРЕДЕЛАЛИ SERVER
            new_message = self.fernet.decryption(message.message)
        else:
            new_message = self.fernet.decryption(message.message)
        sender_name = message.sender_name
        self.db.save_message(new_message)
        self.message.emit(time, sender, sender_name, new_message)

    def get_history(self, id_senders: int, id_recipient: int) -> list[MessageModel] | None:
        return self.db.get_history(id_senders, id_recipient)

    def get_user_chat(self, id_senders: int):
        return self.db.get_user_chats(id_senders)