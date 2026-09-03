from PyQt6.QtCore import QObject

class BaseCommand(QObject):
    def __init__(self, id: int):
        self.id = id

    def execute(self) -> None:
        raise NotImplementedError()

    def undo(self) -> None:
        raise NotImplementedError()