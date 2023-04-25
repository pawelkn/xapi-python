from .socket import Socket
from .stream import Stream
from .exceptions import LoginFailed

class XAPI:
    def __init__(self):
        self.socket = Socket()
        self.stream = Stream()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.disconnect()

    async def disconnect(self):
        await self.socket.disconnect()
        await self.stream.disconnect()

async def connect(
        accountId: str,
        password: str,
        host: str = "ws.xtb.com",
        type: str = "real",
        safe: bool = False
    ):

    x = XAPI()

    x.stream.safe = safe
    x.socket.safe = safe

    if not host.startswith("wss://") and not host.startswith("ws://"):
        host = f"wss://{host}"

    socket_url = f"{host}/{type}"
    stream_url = f"{host}/{type}Stream"

    await x.socket.connect(socket_url)
    await x.stream.connect(stream_url)

    result = await x.socket.login(accountId, password)
    if result['status'] != True:
        raise LoginFailed(result)

    x.stream.streamSessionId = result['streamSessionId']
    return x