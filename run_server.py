import asyncio
from server.core.tcp_server import TcpServer
from server.services.chat_manager import ChatManager
from server.repository.db_repository.sql_lite_message_repository import SqlLiteMessageRepository

async def main():
    db = SqlLiteMessageRepository('greenhouse_sensors.db')
    server = TcpServer()
    manager = ChatManager(server, db)
    server.add_observer(manager)
    await server.start()
    await asyncio.Event().wait()

asyncio.run(main())