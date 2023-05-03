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
        """
        This is an asynchronous function that closes connection to the xStation5 trading platform.
        """

        await self.socket.disconnect()
        await self.stream.disconnect()

async def connect(
        accountId: str,
        password: str,
        host: str = "ws.xtb.com",
        type: str = "real",
        safe: bool = False
    ):
    """
    This is an asynchronous function that establishes a connection to the xStation5 trading platform.

    Parameters
    ----------
    `accountId` : `str`
        User's xStation5 account ID
    `password` : `str`
        User's xStation5 account password
    `host` : `str`, `optional`
        The xStation5 trading platform host name or IP address (default is `ws.xtb.com`)
    `type` : `str`, `optional`
        A type of the xStation5 account, which can be either `real` or `demo` (default is `real`)
    `safe` : `boolean`, `optional`
        A parameter indicating whether the connection should disallow trade execution (default is `False`)

    Returns
    -------
    `XAPI`
        An object of XAPI that can be utilized to communicate with the xStation 5 trading platform.

    Raises
    ------
    `LoginFailed`
        Raised when a log in failed.
    `ConnectionClosed`
        Raised when a connection has never been opened or closed unexpectedly.
    """

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