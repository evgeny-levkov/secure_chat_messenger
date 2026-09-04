from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from .auth_window import AuthWindow
from .chat_window import ChatWindow
from ...viewmodel.client_viewmodel import ClientViewModel


class MainWindow(QMainWindow):
    def __init__(self, viewmodel: ClientViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        self.initialize_ui()
        
    def initialize_ui(self):
        self.setMinimumSize(1200, 800)
        self.stack_widget = QStackedWidget()
        self.auth_window = AuthWindow(self.viewmodel)
        self.chat_window = ChatWindow(self.viewmodel)
        self.stack_widget.addWidget(self.auth_window)
        self.stack_widget.addWidget(self.chat_window)
        self.stack_widget.setCurrentIndex(0)
        self.auth_window.switch_window.connect(self.switch_auth_window)

        self.setCentralWidget(self.stack_widget)

    def switch_auth_window(self, client_id: int):
        self.stack_widget.setCurrentIndex(1)
        self.client_id = client_id
        self.chat_window.chat_list_panel.fill_chats()