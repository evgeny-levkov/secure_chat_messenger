from .base_command import BaseCommand
from ..repositories.base_client_message_repository import BaseClientMessageRepository
from PyQt6.QtCore import pyqtSignal
from ...common.models.message_model import MessageModel


class LocalEditCommand(BaseCommand):
    edit_message = pyqtSignal(MessageModel | None)
    unded = pyqtSignal(MessageModel)
    def __init__(self, id: int, db: BaseClientMessageRepository, message: str):
        super().__init__()
        self.id = id
        self.db = db
        self.message = message
        self.old_massege = None
        self.new_message = None

    def execute(self):
        output = self.db.edit_message(self.id, self.message)
        if output is not None:
            old, edited = output
            if isinstance(edited, MessageModel):
                self.old_massege = old
                self.new_message = edited
            else:
                pass
        self.edit_message.emit(self.new_message)

    def undo(self):
        output = self.db.edit_message(self.id, self.old_massege.message)
        if output is not None:
            old, edited = output
            if isinstance(edited, MessageModel):
                self.old_massege = old
                self.new_message = edited
            else:
                pass
        self.unded.emit(self.new_message)