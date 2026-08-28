from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class AuthRequest:
    name: str
    email: str
    public_key: str

    def to_dict(self) -> dict[str, str]:
        return {'status': 'auth', 'name': self.name, 'email': self.email, 'public_key': self.public_key}

    @classmethod
    def from_dict(cls, model: dict[str, str]) -> AuthRequest | None:
        try:
            return cls(model['name'], model['email'], model['public_key'])
        except Exception as e:
            print(f'Ошибка создания AuthRequest: {e}')
            return None