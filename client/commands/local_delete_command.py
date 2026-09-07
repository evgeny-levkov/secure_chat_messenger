from .base_command import BaseCommand
from ..repositories.base_client_message_repository import BaseClientMessageRepository
from PyQt6.QtCore import pyqtSignal
from common.models.message_model import MessageModel


class LocalDeleteCommand(BaseCommand):
    delete = pyqtSignal(object)
    unded = pyqtSignal(MessageModel)
    def __init__(self, id: str, db: BaseClientMessageRepository) -> None:
        super().__init__()
        self.id = id
        self.db = db
        self._saved_massege = None

    def execute(self) -> None:
        deleted = self.db.delete_message(self.id)
        if isinstance(deleted, MessageModel):
            self._saved_massege = deleted
        else:
            pass
        self.delete.emit(self._saved_massege)

    def undo(self) -> None:
        self.db.save_message(self._saved_massege)
        self.unded.emit(self._saved_massege)