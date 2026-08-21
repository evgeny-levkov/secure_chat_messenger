from .tcp_client_worker import TcpClientWorker
from PyQt6.QtCore import QThread
import asyncio


class TcpClientThread(QThread):
    def __init__(self, worker: TcpClientWorker):
        super().__init__()
        self.worker = worker

    def run(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.worker.read())