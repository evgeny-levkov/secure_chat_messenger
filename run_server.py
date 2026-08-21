import asyncio
from server.core.tcp_server import TcpServer
from server.services.chat_manager import ChatManager

async def main():
    server = TcpServer()
    manager = ChatManager(server)
    server.add_observer(manager)
    await server.start()
    await asyncio.Event().wait()

asyncio.run(main())