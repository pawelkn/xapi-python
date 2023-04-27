from .exceptions import ConnectionClosed

import websockets.client
import websockets.exceptions
import asyncio
import json

class Connection():
    def __init__(self):
        self.safe = False
        self._conn = None

    async def connect(self, url):
        try:
            self._conn = await websockets.client.connect(url, close_timeout=0)

        except asyncio.exceptions.TimeoutError:
            raise ConnectionClosed("Connection timed out")

        except ConnectionRefusedError:
            raise ConnectionClosed("Connection refused")

    async def disconnect(self):
        try:
            if self._conn:
                await self._conn.close()

        except websockets.exceptions.ConnectionClosed:
            pass

        self._conn = None

    async def listen(self):
        try:
            if self._conn:
                async for message in self._conn:
                    yield json.loads(message)
            else:
                raise ConnectionClosed("Not connected")

        except websockets.exceptions.ConnectionClosed:
            self._conn = None
            raise ConnectionClosed("Connection unexpectedly closed")

    async def _request(self, command):
        try:
            if self._conn:
                await self._conn.send(json.dumps(command))
            else:
                raise ConnectionClosed("Not connected")

        except websockets.exceptions.ConnectionClosed:
            self._conn = None
            raise ConnectionClosed("Connection unexpectedly closed")

    async def _response(self):
        try:
            if self._conn:
                response = await self._conn.recv()
                return json.loads(response)
            else:
                raise ConnectionClosed("Not connected")

        except websockets.exceptions.ConnectionClosed:
            self._conn = None
            raise ConnectionClosed("Connection unexpectedly closed")

    async def _transaction(self, command):
        await self._request(command)
        return await self._response()