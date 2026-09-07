from PyQt6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QLabel, QListWidgetItem, QLineEdit, QPushButton, QMessageBox
from ...viewmodel.client_viewmodel import ClientViewModel
from PyQt6.QtCore import Qt, pyqtSignal


class ChatListPanel(QWidget):
    chat_selected = pyqtSignal(int)
    def __init__(self, viewmodel: ClientViewModel) -> None:
        super().__init__()
        self.viewmodel = viewmodel
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
            int_id = int(self.contact_id.text())
            item = QListWidgetItem(f'User{int_id}')
            item.setData(Qt.ItemDataRole.UserRole, int_id)
            self.main_list_box.addItem(item)
        except Exception as e:
            print("Ошибка при добавлении контакта: {e}")
            QMessageBox.critical(self, 'Ошибка', 'Не удалось добавить собеседника')