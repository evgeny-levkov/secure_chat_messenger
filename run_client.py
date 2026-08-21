import asyncio
import json


async def main():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    message = (json.dumps({'status': 'auth', 'name': 'Женя', 'email': 'zhenya@test.com'}) + '\n').encode('utf-8')
    writer.write(message)
    await writer.drain()
    response = await reader.readline()
    print(response.decode('utf-8'))

    my_id = json.loads(response.decode('utf-8') + '\n')['user_id']
    new_messege = (json.dumps({'status': 'send_message', 'message': 'привет!', 'recipient': my_id}))
    writer.write((new_messege + '\n').encode('utf-8'))
    await writer.drain()
    new_response = await reader.readline()
    print(new_response.decode('utf-8'))

asyncio.run(main())