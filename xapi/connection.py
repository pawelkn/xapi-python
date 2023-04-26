from .exceptions import ConnectionClosed

import websockets.client
import websockets.exceptions
import asyncio
import json

class Connection():
    def __init__(self):
        self.safe = False
        self.__conn = None

    async def connect(self, url):
        try:
            self.__conn = await websockets.client.connect(url, close_timeout=0)

        except asyncio.exceptions.TimeoutError:
            raise ConnectionClosed("Connection timed out")

        except ConnectionRefusedError:
            raise ConnectionClosed("Connection refused")

    async def disconnect(self):
        try:
            if self.__conn:
                await self.__conn.close()

        except websockets.exceptions.ConnectionClosed:
            pass

        self.__conn = None

    async def listen(self):
        try:
            if self.__conn:
                async for message in self.__conn:
                    yield json.loads(message)
            else:
                raise ConnectionClosed("Not connected")

        except websockets.exceptions.ConnectionClosed:
            self.__conn = None
            raise ConnectionClosed("Connection unexpectedly closed")

    async def _request(self, command):
        try:
            if self.__conn:
                await self.__conn.send(json.dumps(command))
            else:
                raise ConnectionClosed("Not connected")

        except websockets.exceptions.ConnectionClosed:
            self.__conn = None
            raise ConnectionClosed("Connection unexpectedly closed")

    async def _response(self):
        try:
            if self.__conn:
                response = await self.__conn.recv()
                return json.loads(response)
            else:
                raise ConnectionClosed("Not connected")

        except websockets.exceptions.ConnectionClosed:
            self.__conn = None
            raise ConnectionClosed("Connection unexpectedly closed")

    async def _transaction(self, command):
        await self._request(command)
        return await self._response()