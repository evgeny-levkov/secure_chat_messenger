from dataclasses import dataclass
from typing import Any


@dataclass
class User:
    name: str
    email: str
    id: int | None = None

    def to_dict(self) -> dict[str, str| int | None]:
        return {'id': self.id, 'name': self.name, 'email': self.email}

    @classmethod
    def from_dict(cls, model: dict[str, Any]) -> User | None:
        try:
            return User(model['name'], model['email'], model['id'])
        except Exception as e:
            print(f'Ошибка при создании модели User:{e}')
            return None