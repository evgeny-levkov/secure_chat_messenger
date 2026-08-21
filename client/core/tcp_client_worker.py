from PyQt6.QtCore import QObject, pyqtSignal
import asyncio


class TcpClientWorker(QObject):
    read_signal = pyqtSignal(object)
    async def read(self) -> None:
        self.reader, self.writer = await asyncio.open_connection('127.0.0.1', 8888)
        self.loop = asyncio.get_running_loop()
        while True:
            message = await self.reader.readline()
            if not message:
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