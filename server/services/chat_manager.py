from ..interfaces.base_observer import BaseObserver
from ...common.dto.auth_request import AuthRequest
from ...common.dto.message_request import MessageRequest
from ...common.models.message_model import MessageModel
from ..core.tcp_server import TcpServer
import json
import asyncio
from datetime import datetime


class ChatManager(BaseObserver):
    """Наблюдение за выполнением операций в TCP сервере(Разделение ответственности)"""
    def __init__(self, tcp_server: TcpServer) -> None:
        self.server = tcp_server
        self.senders: dict[tuple[str, int], int] = {}
        self.recipient: dict[int, tuple[str, int]] = {}
        self._user_id = 0

    async def on_message_received(self, client_id: tuple[str, int], message: bytes):
        """ Получаем сообщение из байт -> json. если статуса нет -> выкидываем; если статус auth -> делаем свою модель данных AuthRequest, 
        запоминаем отправителя и получателя; формируем ответ(байты) и отправляем клиенту; если статус send_message -> проверяем что такой
        клиент зарегистрирован, создаём модель MessageRequest из неё формируем ответ сервера через MessageModel и через client_write 
        отправляем получателю."""
        try:
            json_message: dict = json.loads(message)
            if json_message.get('status', None) is None:
                print(f'Неверный формат ответа')
                return None
            elif json_message.get('status', None) == 'auth': 
                if AuthRequest.from_dict(json_message) is not None:
                    self.senders[client_id] = self._user_id
                    self.recipient[self._user_id] = client_id
                    server_req = (json.dumps({f'status': 'auth_success', 'user_id': self._user_id}) + '\n').encode('utf-8')
                    self._user_id += 1
                    write = await self.server.client_write(client_id, server_req)
                else:
                    print('Ошибка при сборе AuthRequest')
                    return None
            elif json_message.get('status') == 'send_message':
                if client_id not in self.senders:
                    print('Такого пользоватлея нет!')
                    return None
                mes_req =  MessageRequest.from_dict(json_message) 
                if mes_req is not None:
                    if mes_req.recipient_id not in self.recipient:
                        print('Клиенты не заригестрированы!!!')
                        return None
                    else:
                        server_req = (json.dumps(MessageModel(mes_req.message, datetime.now(), self.senders.get(client_id), mes_req.recipient_id).to_dict()) + '\n').encode('utf-8') 
                        await self.server.client_write(self.recipient.get(mes_req.recipient_id), server_req)
                else:
                    print('Ошибка при сборе MessageRequest')
                    return None
        except Exception as e:
            print(f'Ошибка обработки ответа: {e}')
            return None

    async def on_client_disconnected(self, client_id: tuple[str, int]) -> bool:
            delete_id: int = self.senders.pop(client_id, None)
            if delete_id is None:
                return False
            elif self.recipient.pop(delete_id, None) is not None:
                return True
            else:
                return False

    async def on_client_connected(self, client_id):
        return await super().on_client_connected(client_id)