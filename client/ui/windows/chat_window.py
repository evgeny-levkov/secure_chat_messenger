from PyQt6.QtWidgets import QWidget, QHBoxLayout
from ...viewmodel.client_viewmodel import ClientViewModel
from client.ui.panels.chat_list_panel import ChatListPanel
from client.ui.panels.current_chat_panel import CurrentChatPanel


class ChatWindow(QWidget):
    def __init__(self, viewmodel: ClientViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        self.initialize_ui()

    def initialize_ui(self):
        self.main_box = QHBoxLayout()
        self.main_box.setContentsMargins(0, 0, 0, 0) 
        self.main_box.setSpacing(0)
        self.chat_list_panel = ChatListPanel(self.viewmodel)
        self.current_chat_panel = CurrentChatPanel(self.viewmodel)
        self.main_box.addWidget(self.chat_list_panel, 1)
        self.main_box.addWidget(self.current_chat_panel, 3)
        self.chat_list_panel.chat_selected.connect(self.conect_current_chat)
        self.setLayout(self.main_box)

    def conect_current_chat(self, current_id: int):
        self.current_chat_panel.get_history(current_id)