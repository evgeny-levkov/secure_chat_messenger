from PyQt6.QtCore import pyqtSignal, QObject
from ..services.base_client_service import BaseClientService
from common.models.message_model import MessageModel
from ..repositories.base_client_message_repository import BaseClientMessageRepository
from ..encryption.encryption_factory import EncryptionFactory
from ..encryption.base_encryption import BaseEncryption
from datetime import datetime
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
import base64


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
        self.client_service.public_key_received.connect(self._on_public_key_received)
        self.db = db
        self.encrytion_keys: dict[int, BaseEncryption] = {}
        self.recipients_public_key: dict[int, str] = {}
        
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
        if self.encrytion_keys.get(recipient_id, None) == None:    
            fernet: BaseEncryption = EncryptionFactory.get_class(encryption)
            fernet.generate_key()
            self.encrytion_keys[recipient_id] = fernet
        if encryption != "Без шифрования":
            rsa = RSA.importKey(self.recipients_public_key[recipient_id])
            cipher_rsa = PKCS1_OAEP.new(rsa)
            new_message = self.encrytion_keys[recipient_id].encryption(message)
            new_encryption = cipher_rsa.encrypt(self.encrytion_keys[recipient_id].key)
            enc_key_str = base64.b64encode(new_encryption).decode('utf-8')
        else:
            new_message = message
            enc_key_str = None
        self.db.save_message(MessageModel(message, time_now, self.my_id, sender_name, recipient_id, encryption, enc_key_str))
        self.client_service.send_message(new_message, recipient_id, sender_name, encryption, enc_key_str)
        self.message.emit(time_now, self.my_id, sender_name, message, encryption)
        
    def _get_send_message(self, message: MessageModel) -> None:
        time = message.time
        sender = message.sender
        encryption = message.encryption
        sender_name = message.sender_name
        if encryption != "Без шифрования":
            rsa_private = RSA.import_key(self.client_service.private_key)
            cipher_rsa = PKCS1_OAEP.new(rsa_private)
            enc_key = base64.b64decode(message.encryption_key)
            enc_key_str = cipher_rsa.decrypt(enc_key).decode('utf-8')
            fernet: BaseEncryption = EncryptionFactory.get_class(encryption)
            fernet.key = enc_key_str
            new_message = fernet.decryption(message.message)
        else:
            new_message = message.message
            enc_key_str = None
        message.message = new_message
        self.db.save_message(message)
        self.message.emit(time, sender, sender_name, new_message, encryption)

    def get_history(self, id_senders: int, id_recipient: int) -> list[MessageModel] | None:
        self.client_service.request_public_key(id_recipient)
        return self.db.get_history(id_senders, id_recipient)

    def get_user_chat(self, id_senders: int):
        return self.db.get_user_chats(id_senders)

    def _on_public_key_received(self, public_key: str, recipient: int):
        self.recipients_public_key[recipient] = public_key