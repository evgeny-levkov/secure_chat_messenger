from ..interfaces.base_observer import BaseObserver
from common.dto.auth_request import AuthRequest
from common.dto.message_request import MessageRequest
from common.models.message_model import MessageModel
from common.models.user_model import UserModel
from ..network.tcp_server import TcpServer
import json
from ..repository.base_server_message_repository import BaseMessageRepository
from datetime import datetime


class ChatManager(BaseObserver):
    """Наблюдение за выполнением операций в TCP сервере(Разделение ответственности)"""
    def __init__(self, tcp_server: TcpServer, db: BaseMessageRepository) -> None:
        self.server = tcp_server
        self.senders: dict[tuple[str, int], int] = {}
        self.recipient: dict[int, tuple[str, int]] = {}
        self.db = db

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
                    user = self.db.check_user(json_message['email'])
                    if user is None:
                        _user_id = self.db.add_new_user(json_message['name'], json_message['email'], json_message['public_key'])
                    else:
                        _user_id = user.id
                    self.senders[client_id] = _user_id
                    self.recipient[_user_id] = client_id
                    server_req = (json.dumps({f'status': 'auth_success', 'user_id':  _user_id}) + '\n').encode('utf-8')
                    write = await self.server.client_write(client_id, server_req)
                else:
                    print('Ошибка при сборе AuthRequest')
                    return None
            elif json_message.get('status') == 'send_message':
                if client_id not in self.senders:
                    print('Такого пользователя нет!')
                    return None
                mes_req =  MessageRequest.from_dict(json_message) 
                if mes_req is not None:
                    if mes_req.recipient_id not in self.recipient:
                        print('Клиенты не заригестрированы!!!')
                        return None
                    else:
                        client_message = MessageModel(mes_req.message, datetime.now(), self.senders.get(client_id), mes_req.sender_name, 
                                                      mes_req.recipient_id, mes_req.encryption, mes_req.encryption_key)
                        server_req = (json.dumps(client_message.to_dict()) + '\n').encode('utf-8') 
                        await self.server.client_write(self.recipient.get(mes_req.recipient_id), server_req)
                        self.db.save_history(client_message)
                else:
                    print('Ошибка при сборе MessageRequest')
                    return None
            elif json_message.get('status', None) == 'get_public_key':
                user_public_key = self.db.get_public_key(json_message['recipient'])
                if user_public_key is None:
                    print('Нет такого user')
                    return None
                else:
                    server_req = (json.dumps({f'status': 'return_public_key', 'public_key': user_public_key,
                                              'recipient': json_message['recipient']}) +  '\n').encode('utf-8')
                    await self.server.client_write(client_id, server_req)
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
        print(f'Новое подключение! Клиент: {client_id}')

    async def get_history(self, id_senders: int, id_recipient: int) -> list[MessageModel] | None:
        return self.db.get_history(id_senders, id_recipient)