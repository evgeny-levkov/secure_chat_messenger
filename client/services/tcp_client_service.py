import asyncio
from PyQt6.QtCore import QObject, pyqtSignal
from .base_client_service import BaseClientService
from common.dto.auth_request import AuthRequest
from common.dto.message_request import MessageRequest
from common.models.message_model import MessageModel
from ..core.tcp_client_thread import TcpClientThread
from ..core.tcp_client_worker import TcpClientWorker
import json


class TcpClientService(BaseClientService):
    connection = pyqtSignal(bool)
    authorization = pyqtSignal(bool, int)
    message = pyqtSignal(object)
    def connect(self, host: str, port: int) -> None:
        self.tcp_worker = TcpClientWorker(host, port)
        self.tcp_thread = TcpClientThread(self.tcp_worker)
        self.tcp_thread.start()
        self.tcp_worker.read_signal.connect(self._on_message_recive)
        self.tcp_worker.connection.connect(self._on_connected)

    def _on_connected(self, con: bool) -> None:
        self.connection.emit(True) if con else self.connection.emit(False)

    def authorize(self, name: str, email: str) -> None:
        auth_message = json.dumps(AuthRequest(name, email).to_dict())
        self.tcp_worker.write(auth_message)

    def send_message(self, message: str, recipient_id: int, sender_name: str, encryption: str) -> None:
        send_message = json.dumps(MessageRequest(message, recipient_id, sender_name, encryption).to_dict())
        self.tcp_worker.write(send_message)

    def _on_message_recive(self, server_answer: str | bool) -> None:
        dict_server_answer: dict = json.loads(server_answer)
        if dict_server_answer.get('status', None) == 'auth_success':
            self.authorization.emit(True, dict_server_answer.get('user_id',None))
        elif dict_server_answer.get('message', None) != None:
            self.message.emit(MessageModel.from_dict(dict_server_answer))