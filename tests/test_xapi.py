import unittest
import time

from xapi import xapi, LoginFailed, ConnectionClosed
from mock_server import MockServer

CREDENTIALS = {
    "accountId": "mockId",
    "password": "mockPasswd",
    "host": f"ws://127.0.0.1:60451"
}

class TestEspiEbiReports(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        cls.mock_server = MockServer("127.0.0.1", 60451)
        time.sleep(.1) # wait for the server to become ready
        pass

    @classmethod
    def tearDownClass(cls):
        cls.mock_server.destroy()
        pass

    async def test_connect(self):
        try:
            x = await xapi.connect(**CREDENTIALS)
            await x.stream.getTickPrices("BITCOIN")

        except LoginFailed as e:
            print(f"Log in failed: {e}")

        except ConnectionClosed as e:
            print(f"Connection closed: {e}")

if __name__ == '__main__':
    unittest.main(exit=False)
    print("all")