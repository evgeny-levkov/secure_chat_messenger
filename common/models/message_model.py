from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class MessageModel:
    message : str
    time: datetime
    sender: int
    sender_name: str
    recipient: int
    id: int | None = None

    def to_dict(self) -> dict[str, str | datetime | int | None]:
        return {'id': self.id, 'message': self.message, 'time': datetime.isoformat(self.time), 'sender': self.sender,
                'sender_name': self.sender_name,'recipient': self.recipient}

    @classmethod
    def from_dict(cls, model: dict[str, Any]) -> MessageModel | None:
        try:
            return MessageModel(model['message'], datetime.fromisoformat(model['time']), model['sender'], model['sender_name'],
                                model['recipient'], model['id'])
        except Exception as e:
            print(f'Ошибка при создании модели Message:{e}')
            return None