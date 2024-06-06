import asyncio
import websockets

class WsServer:

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    async def hello(self, websocket, path):
        name = await websocket.recv()
        print(f"< {name}")

        greeting = f"Hello {name}!"

        print(f"> {greeting}")
        await websocket.send(greeting)

    def start(self):

        start_server = websockets.serve(self.hello, self.host, self.port)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    ws_server = WsServer("localhost", 8765)
    print("hey")
    ws_server.start()
    print("hi")