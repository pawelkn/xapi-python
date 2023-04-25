from .exceptions import ConnectionClosed

import websockets
import asyncio
import json

class Connection:
    def __init__(self):
        self.safe = False

    async def connect(self, url):
        try:
            self.__conn = await websockets.connect(url, close_timeout=0)

        except asyncio.exceptions.TimeoutError:
            raise ConnectionClosed("Connection timed out")

        except ConnectionRefusedError:
            raise ConnectionClosed("Connection refused")

    async def disconnect(self):
        try:
            await self.__conn.close()

        except NameError:
            pass

    async def listen(self):
        try:
            async for message in self.__conn:
                yield json.loads(message)

        except NameError:
            raise ConnectionClosed("Not connected")

        except websockets.ConnectionClosed:
            raise ConnectionClosed("Connection unexpectedly closed")

    async def _request(self, command):
        try:
            await self.__conn.send(json.dumps(command))

        except NameError:
            raise ConnectionClosed("Not connected")

        except websockets.ConnectionClosed:
            raise ConnectionClosed("Connection unexpectedly closed")

    async def _response(self):
        try:
            response = await self.__conn.recv()
            return json.loads(response)

        except NameError:
            raise ConnectionClosed("Not connected")

        except websockets.ConnectionClosed:
            raise ConnectionClosed("Connection unexpectedly closed")

    async def _transaction(self, command):
        await self._request(command)
        return await self._response()