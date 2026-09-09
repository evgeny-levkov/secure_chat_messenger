from abc import ABC, abstractmethod
from common.models.message_model import MessageModel
from common.models.user_model import UserModel


class BaseMessageRepository(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def save_history(self, message: MessageModel) -> None:
        pass

    @abstractmethod
    def get_history(self, id_senders: int, id_recipient: int) -> list[MessageModel] | None:
        pass

    @abstractmethod
    def get_user_chats(self, id_senders: int) -> dict[int, str] | None:
        pass

    @abstractmethod
    def check_user(self, email: str) -> UserModel | None:
        pass

    @abstractmethod
    def add_new_user(self, name: str, email: str, public_key: str) -> int |  None:
        pass

    @abstractmethod
    def get_public_key(self, user_id: int) -> str | None:
        pass

    @abstractmethod
    def delete_message(self, id: str) -> MessageModel | None:
         pass

    @abstractmethod
    def edit_message(self, id: str, message: str) -> tuple[MessageModel, MessageModel] | None:
         pass

    @abstractmethod
    def found_user(self, id: int) -> UserModel | None:
        pass