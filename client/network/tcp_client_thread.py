from .tcp_client_worker import TcpClientWorker
from PyQt6.QtCore import QThread
import asyncio


class TcpClientThread(QThread):
    def __init__(self, worker: TcpClientWorker) -> None:
        super().__init__()
        self.worker = worker

    def run(self) -> None:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.worker.read())