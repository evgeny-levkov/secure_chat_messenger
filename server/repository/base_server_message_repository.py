from abc import ABC, abstractmethod
from common.models.message_model import MessageModel


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