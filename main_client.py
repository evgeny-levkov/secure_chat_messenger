from PyQt6.QtWidgets import QApplication
from client.ui.windows.main_window import MainWindow
from client.viewmodel.client_viewmodel import ClientViewModel
from client.services.tcp_client_service import TcpClientService
from client.repositories.db_repository.sqlite_client_message_repository import SqLiteClientMessageRepository
from Cryptodome.PublicKey import RSA
import sys
import asyncio


def main():
    app = QApplication(sys.argv)
    with open('style.css', 'r', encoding='utf-8') as f:
        app.setStyleSheet(f.read())
    if len(sys.argv) > 1:
        db = SqLiteClientMessageRepository(sys.argv[1])
    else:
        db = SqLiteClientMessageRepository('client_sensor.db')
    keys = db.get_keys()
    if keys is not None:
        client_service = TcpClientService(keys[1], keys[0])
    else:
        keys  = RSA.generate(2048)
        private_key = keys.exportKey(format='PEM').decode('utf-8')
        public_key = keys.publickey().exportKey(format='PEM').decode('utf-8')
        client_service = TcpClientService(public_key, private_key)
        db.save_keys(private_key, public_key)
    viewmodel = ClientViewModel(client_service, db)
    viewmodel.connect('127.0.0.1', 8888)
    wnd = MainWindow(viewmodel)
    wnd.show()

    app.exec()

if __name__ == "__main__":
    main()