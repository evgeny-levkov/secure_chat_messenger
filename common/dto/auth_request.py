from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class AuthRequest:
    name: str
    email: str

    def to_dict(self) -> dict[str, str]:
        return {'status': 'auth', 'name': self.name, 'email': self.email}

    @classmethod
    def from_dict(cls, model: dict[str, str]) -> AuthRequest | None:
        try:
            return cls(model['name'], model['email'])
        except Exception as e:
            print(f'Ошибка создания AuthRequest: {e}')
            return None