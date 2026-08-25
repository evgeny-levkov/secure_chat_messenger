from abc import ABC, abstractmethod
from ...common.models.message_model import MessageModel


class BaseClientMessageRepository(ABC):
    def __init__(self, db: str):
        pass

    @abstractmethod
    def get_history(self, id_senders: int, id_recipient: int) -> list[MessageModel] | None:
        pass

    @abstractmethod
    def save_message(self, message: MessageModel) -> None:
        pass