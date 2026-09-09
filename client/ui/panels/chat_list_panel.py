from PyQt6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QLabel, QListWidgetItem, QLineEdit, QPushButton, QMessageBox
from ...viewmodel.client_viewmodel import ClientViewModel
from PyQt6.QtCore import Qt, pyqtSignal


class ChatListPanel(QWidget):
    chat_selected = pyqtSignal(int)
    def __init__(self, viewmodel: ClientViewModel) -> None:
        super().__init__()
        self.viewmodel = viewmodel
        self.viewmodel.founded_user.connect(self.get_user_name)
        self.viewmodel.not_founded_user.connect(self.user_not_founded)
        self.initialize_ui()

    def initialize_ui(self) -> None:
        self.main_box = QVBoxLayout()
        self.main_box.setContentsMargins(0, 0, 0, 0)
        self.label_add_contact = QLabel('Добавить контакт')
        self.label_add_contact.setStyleSheet("font-size: 17px;")
        self.label_my_id = QLabel('Мой id:')
        self.label_my_id.setStyleSheet("font-size: 12px;")
        self.contact_id = QLineEdit()
        self.contact_id.setPlaceholderText('Введите id пользователя')
        self.add_contact_button = QPushButton('+')
        self.add_contact_button.clicked.connect(self.add_contact)
        self.main_list_box = QListWidget()
        self.main_box.addWidget(self.label_add_contact)
        self.main_box.addWidget(self.label_my_id)
        self.main_box.addWidget(self.contact_id)
        self.main_box.addWidget(self.add_contact_button)
        self.main_list_box.itemClicked.connect(self.get_choosen_chat)
        self.main_box.addWidget(self.main_list_box)
        self.setLayout(self.main_box)

    def fill_chats(self) -> None:
        self.main_list_box.clear()
        chats = self.viewmodel.get_user_chat(self.viewmodel.my_id)
        self.label_my_id.setText(f'Мой id: {self.viewmodel.my_id}')
        for chat in chats:
            if chats[chat] != None:
                item = QListWidgetItem(chats[chat])
                item.setData(Qt.ItemDataRole.UserRole, chat)
                self.main_list_box.addItem(item)
            else:
                item = QListWidgetItem(f'User{chat}')
                item.setData(Qt.ItemDataRole.UserRole, chat)
                self.main_list_box.addItem(item)

    def get_choosen_chat(self, item: QListWidgetItem) -> None:
        self.chat_selected.emit(item.data(Qt.ItemDataRole.UserRole))

    def add_contact(self) -> None:
        try:
            id = int(self.contact_id.text())
            self.viewmodel.found_user(id)
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', 'Ошибка в id')

    def get_user_name(self, id: int, name: str) -> None:
        item = QListWidgetItem(name)
        item.setData(Qt.ItemDataRole.UserRole, id)
        self.main_list_box.addItem(item)

    def user_not_founded(self, status :str) -> None:
        QMessageBox.critical(self, 'Ошибка', 'User не зарегестрирован')