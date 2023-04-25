import unittest

from xapi import xapi, LoginFailed, ConnectionClosed
from mock_server import MockServer

HOST = "localhost"
PORT = 60451

CREDENTIALS = {
    "accountId": "mockId",
    "password": "mockPasswd",
    "host": f"ws://{HOST}:{PORT}"
}

class TestEspiEbiReports(unittest.IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        cls.mock_server = MockServer(HOST, PORT)
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