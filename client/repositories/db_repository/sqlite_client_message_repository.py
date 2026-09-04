from ..base_client_message_repository import BaseClientMessageRepository
from common.models.message_model import MessageModel
from common.models.user_model import UserModel
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
            self.conn.execute('create table if not exists keys(private_key TEXT, public_key TEXT)')
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

    def delete_message(self, id: int) -> MessageModel | None:
        try:
            cur = self.conn.cursor()
            res = cur.execute('DELETE FROM messages WHERE id = ? '\
                        'RETURNING id, message, time, sender, sender_name, recipient, encryption', (id,)).fetchall()
            self.conn.commit()
            if res:
                return MessageModel(message=res[0][1], time=datetime.datetime.fromisoformat(res[0][2]), sender=res[0][3], 
                                    sender_name=res[0][4], recipient=res[0][5], encryption=res[0][6], id=res[0][0])
            else:
                return None
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")
            return None

    def edit_message(self, id: int, message: str):
        try:
            cur = self.conn.cursor()
            old_res = cur.execute('SELECT * from messages WHERE id = ?', (id,)).fetchone()
            new_res = cur.execute('UPDATE messages SET message = ? WHERE id = ? ' \
            'RETURNING id, message, time, sender, sender_name, recipient, encryption', (message, id)).fetchone()
            self.conn.commit()
            if new_res and old_res:
                return (MessageModel(message=old_res[1], time=datetime.datetime.fromisoformat(old_res[2]), sender=old_res[3], 
                                                                    sender_name=old_res[4], recipient=old_res[5], encryption=old_res[6], id=old_res[0]),
                        MessageModel(message=new_res[1], time=datetime.datetime.fromisoformat(new_res[2]), sender=new_res[3], 
                                                    sender_name=new_res[4], recipient=new_res[5], encryption=new_res[6], id=new_res[0]))
            else:
                return None
        except Exception as e:
                print(f"Ошибка при изменении сообщения: {e}")
                return None
    
    def save_keys(self, private_key: str, public_key: str) -> None:
        try:
            cur = self.conn.cursor()
            cur.execute('insert into keys(private_key, public_key) values(?, ?)', (private_key, public_key))
            self.conn.commit()
        except Exception as e:
            print(f'Ошибка сохранения ключей:{e}')
            return None

    def get_keys(self) -> tuple[str, str] | None:
        try:
            cur = self.conn.cursor()
            output = cur.execute('select * from keys').fetchone()
            return output
        except Exception as e:
            print(f'Ошибка получения ключей:{e}')
            return None