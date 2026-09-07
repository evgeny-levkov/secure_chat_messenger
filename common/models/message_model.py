from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class MessageModel:
    uuid: str
    message : str
    time: datetime
    sender: int
    sender_name: str
    recipient: int
    encryption: str | None = None
    encryption_key: str | None = None

    def to_dict(self) -> dict[str, str | datetime | int | None]:
        return {'uuid': self.uuid, 'message': self.message, 'time': datetime.isoformat(self.time), 'sender': self.sender,
                'sender_name': self.sender_name,'recipient': self.recipient, 'encryption': self.encryption, 'encryption_key': self.encryption_key}

    @classmethod
    def from_dict(cls, model: dict[str, Any]) -> MessageModel | None:
        try:
            return MessageModel(model['uuid'], model['message'], datetime.fromisoformat(model['time']), model['sender'], model['sender_name'],
                                model['recipient'], model.get('encryption', None), model.get('encryption_key', None))
        except Exception as e:
            print(f'Ошибка при создании модели Message:{e}')
            return None