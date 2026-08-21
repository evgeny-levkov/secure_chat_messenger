from dataclasses import dataclass
from datetime import datetime


@dataclass
class MessageRequest:
    message : str
    recipient_id: int

    def to_dict(self) -> dict[str, str]:
        return {'status': 'send_message', 'message': self.message, 'recipient': self.recipient_id}

    @classmethod
    def from_dict(cls, model: dict[str, str | int]) -> MessageRequest | None:
        try:
            return cls(model['message'], model['recipient'])
        except Exception as e:
            print(f'Ошибка создания MessegeRequest:{e}')
            return None