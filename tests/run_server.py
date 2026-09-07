import asyncio
from server.network.tcp_server import TcpServer
from server.services.chat_manager import ChatManager
from server.repository.db_repository.sqlite_server_message_repository import SqLiteServerMessageRepository

async def main() -> None:
    db = SqLiteServerMessageRepository('greenhouse_sensors.db')
    server = TcpServer()
    manager = ChatManager(server, db)
    server.add_observer(manager)
    await server.start()
    await asyncio.Event().wait()

asyncio.run(main())