from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLineEdit, QPushButton, QHBoxLayout
from ...viewmodel.client_viewmodel import ClientViewModel
from PyQt6.QtCore import Qt, pyqtSignal
import datetime


class CurrentChatPanel(QWidget):
    def __init__(self, viewmodel: ClientViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        self.initialize_ui()
        self.selected_user_id = None

    def initialize_ui(self):
        self.main_box = QVBoxLayout()
        self.main_box.setContentsMargins(0, 0, 0, 0)
        self.history_message = QListWidget()
        self.lower_panel = QHBoxLayout()
        self.new_messege = QLineEdit()
        self.send_button = QPushButton('Отправить')
        self.send_button.clicked.connect(self.send_message)
        self.lower_panel.addWidget(self.new_messege)
        self.lower_panel.addWidget(self.send_button)
        self.main_box.addWidget(self.history_message)
        self.main_box.addLayout(self.lower_panel)
        self.viewmodel.message.connect(self.update_my_message)
        self.setLayout(self.main_box)

    def get_history(self, selected_user_id: int):
        self.history_message.clear()
        self.selected_user_id = selected_user_id
        hisory = self.viewmodel.get_history(self.viewmodel.my_id, selected_user_id)
        for messege in hisory:
            if messege.sender == self.viewmodel.my_id:
                smb_messege = QListWidgetItem(f'{messege.sender_name}: {messege.message}')
                smb_messege.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                self.history_message.addItem(smb_messege)
            else:
                smb_messege = QListWidgetItem(f'{messege.sender_name}: {messege.message}')
                smb_messege.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
                self.history_message.addItem(smb_messege)

        hisory.clear()

    def send_message(self):
        if self.selected_user_id != None and self.new_messege.text().strip() != '':
            self.viewmodel.send_message(self.new_messege.text(), self.selected_user_id, self.viewmodel.my_name)
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