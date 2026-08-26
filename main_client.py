from PyQt6.QtWidgets import QApplication
from client.ui.windows.main_window import MainWindow
from client.viewmodel.client_viewmodel import ClientViewModel
from client.services.tcp_client_service import TcpClientService
from client.repositories.db_repository.sqlite_client_message_repository import SqLiteClientMessageRepository
import sys
import asyncio


def main():
    app = QApplication(sys.argv)
    with open('style.css', 'r', encoding='utf-8') as f:
        app.setStyleSheet(f.read())
    db = SqLiteClientMessageRepository('client_sensors.db')
    client_service = TcpClientService()
    viewmodel = ClientViewModel(client_service, db)
    viewmodel.connect('127.0.0.1', 8888)
    wnd = MainWindow(viewmodel)
    wnd.show()

    app.exec()

if __name__ == "__main__":
    main()