import websockets
import asyncio
import json
import multiprocessing

class MockServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.proc = multiprocessing.Process(target=self.run, args=())
        self.proc.start()

    def destroy(self):
        self.proc.terminate()

    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # create handler for each connection
            async def handler(websocket, path):
                try:
                    data = await websocket.recv()
                    request = json.loads(data)
                    print(f"Mock Server: client request path: {path}, request: {request}")

                    if path == "/real":
                        if request["command"] == "login":
                            arguments = request["arguments"]
                            if arguments["userId"] == "mockId" and arguments["password"] == "mockPasswd":
                                await websocket.send(json.dumps({"status": True, "streamSessionId": 123}))
                            else:
                                await websocket.send(json.dumps({"status": False, "message": "Incorrect login or password"}))

                    elif path == "/realStream":
                        if request["command"] == "getTickPrices" and request["streamSessionId"] == 123:
                            pass

                except websockets.exceptions.ConnectionClosedOK:
                    pass

                except websockets.exceptions.ConnectionClosedError:
                    pass

            server = websockets.serve(handler, self.host, self.port)
            loop.run_until_complete(server)
            loop.run_forever()

        finally:
            print(f"Mock Server: Server ended")
