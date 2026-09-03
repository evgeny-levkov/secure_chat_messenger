from abc import ABC, abstractmethod
from common.models.message_model import MessageModel


class BaseClientMessageRepository(ABC):
    def __init__(self, db: str):
        pass

    @abstractmethod
    def get_history(self, id_senders: int, id_recipient: int) -> list[MessageModel] | None:
        pass

    @abstractmethod
    def save_message(self, message: MessageModel) -> None:
        pass

    @abstractmethod
    def get_user_chats(self, id_senders: int) -> dict[int, str] | None:
            pass

    @abstractmethod
    def delete_message(self, id: int) -> MessageModel | None:
         pass

    @abstractmethod
    def edit_message(self, id: int, message: str) -> tuple[MessageModel, MessageModel] | None:
         pass