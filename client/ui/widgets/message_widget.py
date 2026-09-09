from PyQt6.QtWidgets import QWidget
from common.models.message_model import MessageModel
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy
from .avatar_widget import AvatarWidget


class MessageWidget(QWidget):
    def __init__(self, message: MessageModel, is_outgoing: bool) -> None:
        super().__init__()
        self.message = message
        self.is_outgoing = is_outgoing
        self.initialize_ui()

    def initialize_ui(self) -> None:
        self.main_box = QHBoxLayout()
        self.bubble = QWidget()
        self.avatar = AvatarWidget(self.message.sender_name)
        self.bubble.setStyleSheet('border-radius: 12px; background-color: #2b5278; padding: 6px 10px')
        self.bubble.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        self.bubble.setMaximumWidth(400)
        self.bubble.setContentsMargins(0,0,0,0)
        self.box = QVBoxLayout()
        self.box.setContentsMargins(1,1,1,1)
        self.text = QLabel(self.message.message)
        self.text.setWordWrap(True)
        self.time = QLabel(str(self.message.time.strftime('%H:%M')))
        self.time.setStyleSheet('font-size: 10px; color: #a0a0a0')
        self.box.addWidget(self.text)
        self.box.addWidget(self.time)

        self.bubble.setLayout(self.box)
        if self.is_outgoing:
            self.main_box.addStretch()
            self.main_box.addWidget(self.bubble)
            self.main_box.addWidget(self.avatar)
        else:
            self.main_box.addWidget(self.avatar)
            self.main_box.addWidget(self.bubble)
            self.main_box.addStretch()
        self.setLayout(self.main_box)