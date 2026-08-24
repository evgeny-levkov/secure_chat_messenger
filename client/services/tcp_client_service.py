import asyncio
from PyQt6.QtCore import QObject, pyqtSignal
from ...common.dto.auth_request import AuthRequest
from ...common.dto.message_request import MessageRequest
from ...common.models.message_model import MessageModel
from ..core.tcp_client_thread import TcpClientThread
from ..core.tcp_client_worker import TcpClientWorker
import json


class TcpClientService(QObject):
    connection = pyqtSignal(bool)
    authorization = pyqtSignal(bool)
    message = pyqtSignal(object)

    def connect(self, host: str, port: int):
        self.tcp_worker = TcpClientWorker(host, port)
        self.tcp_thread = TcpClientThread(self.tcp_worker)
        self.tcp_thread.start()
        self.tcp_worker.read_signal.connect(self._on_message_recive)
        self.tcp_worker.connection.connect(self._on_connected)

    def _on_connected(self):
        self.connection.emit(True)

    def authorize(self, name: str, email: str) -> None:
        auth_message = json.dumps(AuthRequest(name, email).to_dict())
        self.tcp_worker.write(auth_message)

    def send_message(self, message: str, recipient_id: int):
        send_message = json.dumps(MessageRequest(message, recipient_id).to_dict())
        self.tcp_worker.write(send_message)

    def _on_message_recive(self, server_answer: str):
        dict_server_answer: dict = json.loads(server_answer)
        if dict_server_answer.get('status', None) == 'auth_success':
            self.authorization.emit(True)
        elif dict_server_answer.get('message', None) != None:
            self.message.emit(MessageModel.from_dict(dict_server_answer))