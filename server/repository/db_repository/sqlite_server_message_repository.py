from ..base_server_message_repository import BaseMessageRepository
from common.models.message_model import MessageModel
from common.models.user_model import UserModel
import sqlite3
import datetime


class SqLiteServerMessageRepository(BaseMessageRepository):
    def __init__(self, db: str) -> None:
        self.db = db
        self.connection()

    def connection(self) -> None:
        try:
            self.conn = sqlite3.connect(self.db, check_same_thread = False)
        except Exception as e:
            print(f"Ошибка подключения к БД: {e}")
        try:
            cur = self.conn.cursor()
            cur.execute('create table if not exists messages(uuid VARCHAR PRIMARY KEY, message TEXT, time DATETIME, ' \
                'sender INT, sender_name VARCHAR(255), recipient INT, encryption VARCHAR(255))')
            cur.execute('create table if not exists users(id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, email TEXT, public_key TEXT)')
        except Exception as e:
            print(f'Ошибка подключения: {e}')

    def save_history(self, message: MessageModel) -> None:
        cur = self.conn.cursor()
        cur.execute('insert into messages(uuid, message, time, sender, sender_name, recipient, encryption) values (?, ?, ?, ?, ?, ?, ?)', 
                    (message.uuid, message.message, message.time, message.sender, message.sender_name, message.recipient, message.encryption))
        self.conn.commit()

    def get_history(self, id_senders: int, id_recipient: int) -> list[MessageModel] | None:
        res = []
        try:
            cur = self.conn.cursor()
            output = cur.execute('select * from messages where (sender = ? and recipient = ?) or (sender = ? and recipient = ?)', 
                                 (id_senders, id_recipient, id_recipient, id_senders)).fetchall()
            if output is not None:
                for messages in output:
                    res.append(MessageModel(message=messages[1], time=datetime.datetime.fromisoformat(messages[2]), sender=messages[3], 
                                            sender_name=messages[4], recipient=messages[5], encryption=messages[6], uuid=messages[0]))
            else:
                return None
        except Exception as e:
            print(f'Ошибка загрузки данных: {e}')
            return None
        return res

    def get_user_chats(self, id_senders: int) -> dict[int, str] | None:
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

    def add_new_user(self, name: str, email: str, public_key: str) -> int |  None:
        try:
            cur = self.conn.cursor()
            new_id = cur.execute('insert into users(user, email, public_key) ' \
                        'values(?,?,?) RETURNING id', (name, email, public_key)).fetchone()
            self.conn.commit()
            return int(new_id[0])
        except Exception as e:
            print(f'Ошибка при создании User:{e}')

    def check_user(self, email: str) -> UserModel | None:
        try:
            cur = self.conn.cursor()
            output = cur.execute('SELECT * from users where email = ?', (email,)).fetchone()
            if output is not None:
                return UserModel(user=output[1], email=output[2], public_key=output[3], id=output[0])
            else:
                return None
        except Exception as e:
            print(f'Ошибка получения User:{e}')
            return None

    def get_public_key(self, user_id: int) -> str | None:
        try:
            cur = self.conn.cursor()
            user_public_key = cur.execute('SELECT public_key from users where id = ?', (user_id,)).fetchone()
            if user_public_key is not None:
                return user_public_key[0]
            else:
                return None
        except Exception as e:
            print(f'Ошибка при получении public_key: {e}')
            return None

    def delete_message(self, uuid: str)  -> MessageModel | None:
        try:
            cur = self.conn.cursor()
            output = cur.execute('DELETE FROM messages WHERE uuid = ? '\
                        'RETURNING uuid, message, time, sender, sender_name, recipient, encryption', (uuid,)).fetchall()
            self.conn.commit()
            if output:
                return MessageModel(message=output[0][1], time=datetime.datetime.fromisoformat(output[0][2]), sender=output[0][3], 
                                                    sender_name=output[0][4], recipient=output[0][5], encryption=output[0][6], uuid=output[0][0])
            else:
                return None
        except Exception as e:
                print(f"Ошибка при удалении сообщения: {e}")
                return None

    def edit_message(self, id: str, message: str) -> tuple[MessageModel, MessageModel] | None:
        try:
            cur = self.conn.cursor()
            old_res = cur.execute('SELECT * from messages WHERE uuid = ?', (id,)).fetchone()
            new_res = cur.execute('UPDATE messages SET message = ? WHERE uuid = ? ' \
            'RETURNING uuid, message, time, sender, sender_name, recipient, encryption', (message, id)).fetchone()
            self.conn.commit()
            if new_res and old_res:
                return (MessageModel(message=old_res[1], time=datetime.datetime.fromisoformat(old_res[2]), sender=old_res[3], 
                            sender_name=old_res[4], recipient=old_res[5], encryption=old_res[6], uuid=old_res[0]),
                        MessageModel(message=new_res[1], time=datetime.datetime.fromisoformat(new_res[2]), sender=new_res[3], 
                            sender_name=new_res[4], recipient=new_res[5], encryption=new_res[6], uuid=new_res[0]))
            else:
                return None
        except Exception as e:
            print(f"Ошибка при изменении сообщения: {e}")
            return None