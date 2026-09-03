from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLineEdit, QPushButton, QHBoxLayout, QComboBox, QMenu
from PyQt6.QtGui import QShortcut, QKeySequence
from ...viewmodel.client_viewmodel import ClientViewModel
from PyQt6.QtCore import Qt, pyqtSignal, QPoint
import datetime


class CurrentChatPanel(QWidget):
    fernet = pyqtSignal(str)
    edit = pyqtSignal(bool)
    delete = pyqtSignal(bool)
    def __init__(self, viewmodel: ClientViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        self.initialize_ui()
        self.selected_user_id = None

    def initialize_ui(self):
        self.main_box = QVBoxLayout()
        self.main_box.setContentsMargins(0, 0, 0, 0)
        self.history_message = QListWidget()
        self.history_message.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.history_message.customContextMenuRequested.connect(self._show_context_menu)
        self.lower_panel = QHBoxLayout()
        self.new_messege = QLineEdit()
        self.send_button = QPushButton('Отправить')
        self.fernet = QComboBox()
        self.fernet.addItems(['Fernet', 'Без шифрования'])
        self.send_button.clicked.connect(self.send_message)
        self.lower_panel.addWidget(self.new_messege)
        self.lower_panel.addWidget(self.send_button)
        self.lower_panel.addWidget(self.fernet)
        self.main_box.addWidget(self.history_message)
        self.main_box.addLayout(self.lower_panel)
        self.viewmodel.message.connect(self.update_my_message)
        self.viewmodel.deleted_message.connect(self.update_changed_messades)
        self.viewmodel.edited_message.connect(self.update_changed_messades)
        self.viewmodel.undo_delete_message.connect(self.update_changed_messades)
        self.viewmodel.undo_edit_message.connect(self.update_changed_messades)
        self.shortcut_undo = QShortcut(QKeySequence("Ctrl+Z"), self)
        self.shortcut_undo.activated.connect(self.undo)
        self.shortcut_redo = QShortcut(QKeySequence("Ctrl+Shift+Z"), self)
        self.shortcut_redo.activated.connect(self.redo)
        self.setLayout(self.main_box)

    def get_history(self, selected_user_id: int):
        self.history_message.clear()
        self.selected_user_id = selected_user_id
        hisory = self.viewmodel.get_history(self.viewmodel.my_id, selected_user_id)
        for messege in hisory:
            if messege.sender == self.viewmodel.my_id:
                smb_messege = QListWidgetItem(f'{messege.sender_name}: {messege.message}')
                smb_messege.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                smb_messege.setData(Qt.ItemDataRole.UserRole, messege.id)
                self.history_message.addItem(smb_messege)
            else:
                smb_messege = QListWidgetItem(f'{messege.sender_name}: {messege.message}')
                smb_messege.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
                smb_messege.setData(Qt.ItemDataRole.UserRole, messege.id)
                self.history_message.addItem(smb_messege)

        hisory.clear()

    def send_message(self):
        if self.selected_user_id != None and self.new_messege.text().strip() != '':
            self.viewmodel.send_message(self.new_messege.text(), self.selected_user_id, self.viewmodel.my_name, self.fernet.currentText())
            self.new_messege.clear()

    def update_my_message(self, time_now: datetime, my_id: int, sender_name: str, message: str):
        if my_id != self.viewmodel.my_id and my_id != self.selected_user_id:
            return
        elif my_id == self.viewmodel.my_id:
            smb_messege = QListWidgetItem(f'{sender_name}: {message}')
            smb_messege.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            self.history_message.addItem(smb_messege)
        else:
            smb_messege = QListWidgetItem(f'{sender_name}: {message}')
            smb_messege.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            self.history_message.addItem(smb_messege)

    def _show_context_menu(self, pos: QPoint):
        item = self.history_message.itemAt(pos) 
        if item is None:
            return
        menu = QMenu(self)
        action_edit = menu.addAction("Редактировать")
        action_delete = menu.addAction("Удалить")
        action = menu.exec(self.history_message.mapToGlobal(pos))
        if action == action_edit:
            menu.close()
            self.viewmodel.edit_message(self.new_messege.text(), item.data(Qt.ItemDataRole.UserRole))
        elif action == action_delete:
            menu.close()
            self.viewmodel.delete_message(item.data(Qt.ItemDataRole.UserRole))

    def update_changed_messades(self, *args):
        if self.selected_user_id is not None:
            self.get_history(self.selected_user_id)
        else:
            pass

    def undo(self):
        self.viewmodel.undo()

    def redo(self):
        self.viewmodel.redo()