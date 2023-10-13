from .exceptions import ConnectionClosed

import websockets.client
import websockets.exceptions
import socket
import asyncio
import json
import time

class Connection():
    def __init__(self):
        self.safe = False
        self._conn = None
        self._lock = asyncio.Lock()
        self._last_request_time = None

    def skip_delay(self):
        """Dispatch the next request without the 200ms delay"""
        self._last_request_time = None

    async def connect(self, url):
        try:
            self._conn = await websockets.client.connect(url, close_timeout=0, max_size=None)

        except websockets.exceptions.WebSocketException as e:
            raise ConnectionClosed(f"WebSocket exception: {e}")

        except socket.gaierror:
            raise ConnectionClosed("Hostname cannot be resolved")

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

        except websockets.exceptions.WebSocketException as e:
            self._conn = None
            raise ConnectionClosed(f"WebSocket exception: {e}")

    async def _request(self, command):
        if self._last_request_time is not None:
            elapsed_time = time.time() - self._last_request_time
            if elapsed_time < 0.2:
                await asyncio.sleep(0.2 - elapsed_time)

        try:
            if self._conn:
                await self._conn.send(json.dumps(command))
                self._last_request_time = time.time()
            else:
                raise ConnectionClosed("Not connected")

        except websockets.exceptions.WebSocketException as e:
            self._conn = None
            raise ConnectionClosed(f"WebSocket exception: {e}")

    async def _transaction(self, command):
        async with self._lock:
            try:
                if self._conn:
                    await self._request(command)
                    response = await self._conn.recv()
                    return json.loads(response)
                else:
                    raise ConnectionClosed("Not connected")

            except websockets.exceptions.WebSocketException as e:
                self._conn = None
                raise ConnectionClosed(f"WebSocket exception: {e}")