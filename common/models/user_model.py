from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any

@dataclass
class UserModel:
    user: str
    email: str
    public_key: str
    id: int | None = None

    def to_dict(self) -> dict[str, str | int | None]:
        return {'id': self.id, 'user': self.user, 'email': self.email, 'public_key': self.public_key}

    @classmethod
    def from_dict(cls, model: dict[str, str | int | None]) -> UserModel | None:
        try:
            return UserModel(user=model['user'], email=model['email'], public_key=model['public_key'], id=model['id'])
        except Exception as e:
            print(f'Ошибка при создании User:{e}')
            return None