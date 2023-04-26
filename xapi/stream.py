from .connection import Connection


class Stream(Connection):

    def __init__(self):
        super().__init__()
        self.streamSessionId = str()

    async def getBalance(self):
        return await self._request({
            "command": "getBalance",
            "streamSessionId": self.streamSessionId
        })

    async def stopBalance(self):
        return await self._request({
            "command": "stopBalance"
        })

    async def getCandles(self, symbol: str):
        return await self._request({
            "command": "getCandles",
            "streamSessionId": self.streamSessionId,
            "symbol": symbol
        })

    async def stopCandles(self, symbol: str):
        return await self._request({
            "command": "stopCandles",
            "symbol": symbol
        })

    async def getKeepAlive(self):
        return await self._request({
            "command": "getKeepAlive",
            "streamSessionId": self.streamSessionId
        })

    async def stopKeepAlive(self):
        return await self._request({
            "command": "stopKeepAlive"
        })

    async def getNews(self):
        return await self._request({
            "command": "getNews",
            "streamSessionId": self.streamSessionId
        })

    async def stopNews(self):
        return await self._request({
            "command": "stopNews"
        }
        )

    async def getProfits(self):
        return await self._request({
            "command": "getProfits",
            "streamSessionId": self.streamSessionId
        })

    async def stopProfits(self):
        return await self._request({
            "command": "stopProfits"
        })

    async def getTickPrices(self, symbol: str, minArrivalTime: int = 0, maxLevel: int = 2):
        return await self._request({
            "command": "getTickPrices",
            "streamSessionId": self.streamSessionId,
            "symbol": symbol,
            "minArrivalTime": minArrivalTime,
            "maxLevel": maxLevel
        })

    async def stopTickPrices(self, symbol: str):
        return await self._request({
            "command": "stopTickPrices",
            "symbol": symbol
        })

    async def getTrades(self):
        return await self._request({
            "command": "getTrades",
            "streamSessionId": self.streamSessionId
        })

    async def stopTrades(self):
        return await self._request({
            "command": "stopTrades"
        })

    async def getTradeStatus(self):
        return await self._request({
            "command": "getTradeStatus",
            "streamSessionId": self.streamSessionId
        })

    async def stopTradeStatus(self):
        return await self._request({
            "command": "stopTradeStatus"
        })

    async def ping(self):
        return await self._request({
            "command": "ping",
            "streamSessionId": self.streamSessionId
        })
