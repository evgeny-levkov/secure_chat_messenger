from PyQt6.QtCore import QObject, pyqtSignal
import asyncio


class TcpClientWorker(QObject):
    read_signal = pyqtSignal(str)
    connection = pyqtSignal(bool)
    def __init__(self, host: str, port: int) -> None:
        super().__init__()
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        self.connection.emit(True)

    async def read(self) -> None:
        self.loop = asyncio.get_running_loop()
        await self.connect()
        while True:
            message = await self.reader.readline()
            if not message:
                self.reader = None
                self.writer = None
                self.connection.emit(False)
                break
            self.read_signal.emit(message.decode('utf-8'))

    def write(self, message: str) -> None:
       write_message = (message + '\n').encode('utf-8')
       if self.writer is not None:
            corutine = self._async_write(write_message)
            asyncio.run_coroutine_threadsafe(corutine, self.loop)

    async def _async_write(self, message: bytes) -> None:
        self.writer.write(message)
        await self.writer.drain()