from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
from PyQt6.QtCore import Qt
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
        self.card = QFrame()
        self.name_label = QLabel('Введите имя пользователя:')
        self.name_widget = QLineEdit()
        self.email_label = QLabel('Введите email:')
        self.email_widget = QLineEdit()
        self.auth_button = QPushButton('Авторизоваться')
        self.auth_button.clicked.connect(self.authorize)

        self.card_box = QVBoxLayout()
        self.card_box.addWidget(self.name_label)
        self.card_box.addWidget(self.name_widget)
        self.card_box.addWidget(self.email_label)
        self.card_box.addWidget(self.email_widget)
        self.card_box.addWidget(self.auth_button)
        self.card.setLayout(self.card_box)
        self.card.setFixedWidth(500)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.card, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)

    def authorize(self) -> None:
        self.viewmodel.authorization(self.name_widget.text(), self.email_widget.text())

    def get_switch_window(self, sig: bool, client_id: int) -> None:
        if sig:
            self.switch_window.emit(client_id)
        else:
            QMessageBox.critical(self, 'Ошибка авторизации', 'Неверное имя или пароль')