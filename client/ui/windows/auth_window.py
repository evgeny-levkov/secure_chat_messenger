from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import pyqtSignal
from ...viewmodel.client_viewmodel import ClientViewModel


class AuthWindow(QWidget):
    switch_window = pyqtSignal(int)
    def __init__(self, viewmodel: ClientViewModel) -> None:
        super().__init__()
        self.viewmodel = viewmodel
        self.initialize_ui()
        self.viewmodel.authorized.connect(self.get_switch_window)

    def initialize_ui(self) -> None:
        self.main_layout = QVBoxLayout()
        self.name_label = QLabel('Введите имя пользователя:')
        self.name_widget = QLineEdit()
        self.email_label = QLabel('Введите email:')
        self.email_widget = QLineEdit()
        self.auth_button = QPushButton('Авторизоваться')
        self.auth_button.clicked.connect(self.authorize)

        self.main_layout.addWidget(self.name_label)
        self.main_layout.addWidget(self.name_widget)
        self.main_layout.addWidget(self.email_label)
        self.main_layout.addWidget(self.email_widget)
        self.main_layout.addWidget(self.auth_button)

        self.setLayout(self.main_layout)

    def authorize(self) -> None:
        self.viewmodel.authorization(self.name_widget.text(), self.email_widget.text())

    def get_switch_window(self, sig: bool, client_id: int) -> None:
        if sig:
            self.switch_window.emit(client_id)
        else:
            QMessageBox.critical(self, 'Ошибка авторизации', 'Неверное имя или пароль')