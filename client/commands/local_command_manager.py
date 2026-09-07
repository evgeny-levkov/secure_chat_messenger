from .base_command import BaseCommand


class LocalCommandManager():
    def __init__(self):
        self.undo_stack = []#стек отмены
        self.redo_stack = []#стек повтора

    def execute(self, command: BaseCommand) -> None:
        command.execute()
        self.redo_stack.clear()
        self.undo_stack.append(command)

    def undo(self) -> None:
        if self.undo_stack:
            command: BaseCommand = self.undo_stack[-1]
            command.undo()
            self.undo_stack.pop(-1)
            self.redo_stack.append(command)

    def redo(self) -> None:
        if self.redo_stack:
            command: BaseCommand = self.redo_stack[-1]
            command.execute()
            self.redo_stack.pop(-1) 
            self.undo_stack.append(command)