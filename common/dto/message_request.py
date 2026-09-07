from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MessageRequest:
    uuid: str
    message : str
    recipient_id: int
    sender_name: str
    encryption: str | None = None
    encryption_key: str | None = None
    

    def to_dict(self) -> dict[str, str]:
        return {'status': 'send_message', 'message': self.message,'recipient': self.recipient_id, 'sender_name': self.sender_name, 
                'encryption': self.encryption, 'encryption_key': self.encryption_key, 'uuid': self.uuid}

    @classmethod
    def from_dict(cls, model: dict[str, str | int]) -> MessageRequest | None:
        try:
            return cls(model['uuid'], model['message'], model['recipient'], model['sender_name'], model.get('encryption', None), 
                       model.get('encryption_key', None))
        except Exception as e:
            print(f'Ошибка создания MessegeRequest:{e}')
            return None