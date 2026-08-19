import asyncio


class TcpServer():
    def __init__(self):
        self.server = None
        self.writers = {}

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')
        self.writers[addr] = writer
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                
                writer.write(data)
                await writer.drain() 
        except asyncio.CancelledError:
            pass
        finally:
            self.writers.pop(addr)
            print(f"Клиент отключился: {addr}")
            writer.close()
            await writer.wait_closed()

    async def start(self, host, port, limit, ssl_handshake_timeout):
        self.server = await asyncio.start_server(self.handle_client, host, port, limit, ssl_handshake_timeout)