from ..base_client_message_repository import BaseClientMessageRepository
from common.models.message_model import MessageModel
import sqlite3
import datetime


class SqLiteClientMessageRepository(BaseClientMessageRepository):
    def __init__(self, db) -> None:
        self.db = db
        self.connect()

    def connect(self) -> None:
        try:
            self.conn = sqlite3.connect(self.db, check_same_thread = False)
            self.conn.execute('create table if not exists messages(id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT, time DATETIME, ' \
            'sender INT, sender_name VARCHAR(255), recipient INT, encryption VARCHAR(255))')
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")

    def get_history(self, id_senders: int, id_recipient: int) -> list[MessageModel] | None:
        res = []
        try:
            cur = self.conn.cursor()
            output = cur.execute('select * from messages where (sender = ? and recipient = ?) or (sender = ? and recipient = ?)', 
                                (id_senders, id_recipient, id_recipient, id_senders)).fetchall()
            if output is not None:
                for messages in output:
                    res.append(MessageModel(message=messages[1], time=datetime.datetime.fromisoformat(messages[2]), sender=messages[3], 
                                            sender_name=messages[4], recipient=messages[5],  encryption=messages[6], id=messages[0]))
            else:
                return None
        except Exception as e:
            print(f'Ошибка загрузки данных: {e}')
            return None
        return res

    def save_message(self, message: MessageModel) -> None:
        cur = self.conn.cursor()
        cur.execute('insert into messages(id, message, time, sender, sender_name, recipient, encryption) values (?, ?, ?, ?, ?, ?, ?) ' \
        'ON CONFLICT (id) DO NOTHING', (message.id, message.message, message.time, message.sender, message.sender_name, message.recipient, message.encryption))
        self.conn.commit()

    def get_user_chats(self, id_senders):
        res = {}
        try:
            cur = self.conn.cursor()
            output = cur.execute('SELECT DISTINCT user_id, (SELECT sender_name FROM messages WHERE sender = user_id LIMIT 1) AS name ' \
                'FROM (SELECT recipient AS user_id FROM messages WHERE sender = ? '
                    'UNION '\
                'SELECT sender AS user_id FROM messages WHERE recipient = ?) AS partners;', 
                (id_senders, id_senders)).fetchall()
            if output is not None:
                for chats in output:
                    res[chats[0]] = chats[1]
        except Exception as e:
            print(f'Ошибка загрузки данных: {e}')
            return None
        return res