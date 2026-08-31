import asyncio
from PyQt6.QtCore import QObject, pyqtSignal
from .base_client_service import BaseClientService
from common.dto.auth_request import AuthRequest
from common.dto.message_request import MessageRequest
from common.models.message_model import MessageModel
from ..core.tcp_client_thread import TcpClientThread
from ..core.tcp_client_worker import TcpClientWorker
import json
from Cryptodome.PublicKey import RSA


class TcpClientService(BaseClientService):
    connection = pyqtSignal(bool)
    authorization = pyqtSignal(bool, int)
    message = pyqtSignal(object)
    public_key_received = pyqtSignal(str, int)
    def __init__(self):
        super().__init__()
        key = RSA.generate(2048)
        self.public_key = key.publickey().exportKey().decode('utf-8')
        self.private_key = key.exportKey().decode('utf-8')
        
    def connect(self, host: str, port: int) -> None:
        self.tcp_worker = TcpClientWorker(host, port)
        self.tcp_thread = TcpClientThread(self.tcp_worker)
        self.tcp_thread.start()
        self.tcp_worker.read_signal.connect(self._on_message_recive)
        self.tcp_worker.connection.connect(self._on_connected)

    def _on_connected(self, con: bool) -> None:
        self.connection.emit(True) if con else self.connection.emit(False)

    def authorize(self, name: str, email: str) -> None:
        auth_message = json.dumps(AuthRequest(name, email, self.public_key).to_dict())
        self.tcp_worker.write(auth_message)

    def request_public_key(self, recipient_id: int) -> None:
        auth_message = json.dumps({'status': 'get_public_key', 'recipient': recipient_id})
        self.tcp_worker.write(auth_message)

    def send_message(self, message: str, recipient_id: int, sender_name: str, encryption: str, encryption_key: str) -> None:
        send_message = json.dumps(MessageRequest(message, recipient_id, sender_name, encryption, encryption_key).to_dict())
        self.tcp_worker.write(send_message)

    def _on_message_recive(self, server_answer: str | bool) -> None:
        dict_server_answer: dict = json.loads(server_answer)
        if dict_server_answer.get('status', None) == 'auth_success':
            self.authorization.emit(True, dict_server_answer.get('user_id',None))
        elif dict_server_answer.get('message', None) != None:
            self.message.emit(MessageModel.from_dict(dict_server_answer))
        elif dict_server_answer.get('status', None) == 'return_public_key':
            self.public_key_received.emit(dict_server_answer.get('public_key', None), dict_server_answer.get('recipient', None))