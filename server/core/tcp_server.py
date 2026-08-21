import asyncio
from typing import Callable
from ..interfaces.base_observer import BaseObserver


class TcpServer():
    """Ассинхронный TCP сервер с воможность: запуск, чтение сообщений, вывода сообщений"""
    def __init__(self) -> None:
        self.writers = {}
        self._observers = []
        
    async def client_read(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Для каждого подключённого запускаем on_client_connected, читаем сообщения подключённых писателей, для каждого вызываем 
        on_message_received перед выходом запускаем on_client_disconnected и удаляем подключённого писателя"""
        self.writers[writer.get_extra_info('peername')] = writer
        call = await asyncio.gather(*[obs.on_client_connected(writer.get_extra_info('peername')) for obs in self._observers 
                               if isinstance(obs, BaseObserver)])
        try:
            while True:
                message = await reader.readline()
                if not message:
                    break
                call = await asyncio.gather(*[obs.on_message_received(writer.get_extra_info('peername'), message) for obs in self._observers 
                                       if isinstance(obs, BaseObserver)])
        except Exception as e:
            print(f'Ошибка при чтении сообщения:{e}')
            return 
        finally:
            call = await asyncio.gather(*[obs.on_client_disconnected(writer.get_extra_info('peername')) for obs in self._observers 
                                   if isinstance(obs, BaseObserver)])
            self.writers.pop(writer.get_extra_info('peername'))
            writer.close()
            await writer.wait_closed()

    async def client_write(self, peername: tuple[str, int], message: bytes) -> None:
        """После проверки что писатель существует, записываем в поток вывода сообщение писателя через write и отправляем в сеть через await"""
        try:
            writer = self.writers.get(peername, None)
            if writer is not None and isinstance(writer, asyncio.StreamWriter):
                writer.write(message)
                await writer.drain()
            else:
                print('Нет такого writer')
                return 
        except Exception as e:
            print(f'Ошибка: {e}')
            return None

    async def start(self) -> None:
        """Ассинхронный запуск сервера с передачей функции чтения подключившихся клиентов"""
        self.server = await asyncio.start_server(self.client_read, '127.0.0.1', 8888)

    def add_observer(self, observer: BaseObserver) -> None:
        """Добавляем наблюдателя"""
        self._observers.append(observer)

    def remove_observer(self, observer: BaseObserver) -> bool:
        """Удаляем наблюдателя"""
        for obs in self._observers:
            if obs == observer:
                self._observers.remove(obs)
                return True
        return False