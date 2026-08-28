from typing import Callable
from .base_encryption import BaseEncryption


class EncryptionFactory:
    _encryptions = {}
    @classmethod
    def register_encryption(cls, name: str) -> Callable:
        def decorator(class_name: BaseEncryption) -> type[BaseEncryption]:
            cls._encryptions[name] = class_name
            return class_name
        return decorator

    @classmethod
    def get_class(cls, name: str) -> type[BaseEncryption] | None:
        try:
            return cls._encryptions[name]()
        except Exception as e:
            print(f'Ошибка: {e}')
            return None