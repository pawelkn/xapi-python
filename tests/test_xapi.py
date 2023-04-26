import unittest
from unittest.mock import AsyncMock, patch

from xapi import connect, XAPI, Socket, Stream, LoginFailed

class TestXAPI(unittest.IsolatedAsyncioTestCase):

    async def test_xapi(self):
        async with XAPI() as x:
            self.assertIsInstance(x.socket, Socket)
            self.assertIsInstance(x.stream, Stream)

    @patch('xapi.xapi.Stream', return_value=AsyncMock())
    @patch('xapi.xapi.Socket', return_value=AsyncMock())
    async def test_connect_successful_login(self, SocketMock, _):
        SocketMock().login.return_value = {"status": True, "streamSessionId": "abc123"}

        async with await connect("myaccount", "mypassword", "ws.xtb.com", "real", False) as x:
            self.assertIsInstance(x, XAPI)

            self.assertEqual(x.stream.safe, False)
            self.assertEqual(x.socket.safe, False)
            self.assertEqual(x.stream.streamSessionId, "abc123")

            x.socket.connect.assert_called_once_with("wss://ws.xtb.com/real")
            x.stream.connect.assert_called_once_with("wss://ws.xtb.com/realStream")
            x.socket.login.assert_called_once_with("myaccount", "mypassword")

    @patch('xapi.xapi.Stream', return_value=AsyncMock())
    @patch('xapi.xapi.Socket', return_value=AsyncMock())
    async def test_connect_failed_login(self, SocketMock, _):
        SocketMock().login.return_value = AsyncMock(return_value = {"status": False, "errorCode": 1001})

        with self.assertRaises(LoginFailed):
            await connect("myaccount", "mypassword", "ws.xtb.com", "real", False)
