from .connection import Connection
from .enums import TradeCmd, TradeType, PeriodCode

from typing import List

class Socket(Connection):

    async def login(self, accountId: str, password: str):
        return await self._transaction({
            "command": "login",
            "arguments": {
                "userId": accountId,
                "password": password
            }
        })

    async def logout(self):
        return await self._transaction({
            "command": "logout"
        })

    async def getAllSymbols(self):
        return await self._transaction({
            "command": "getAllSymbols"
        })

    async def getCalendar(self):
        return await self._transaction({
            "command": "getCalendar"
        })

    async def getChartLastRequest(self, symbol: str, start: int, period: PeriodCode):
        return await self._transaction({
            "command": "getChartLastRequest",
            "arguments": {
                "info": {
                    "period": period.value,
                    "start": start,
                    "symbol": symbol
                }
            }
        })

    async def getChartRangeRequest(self, symbol: str, start: int, end: int, period: PeriodCode, ticks: int):
        return await self._transaction({
            "command": "getChartRangeRequest",
            "arguments": {
                "info": {
                    "end": end,
                    "period": period.value,
                    "start": start,
                    "symbol": symbol,
                    "ticks": ticks
                }
            }
        })

    async def getCommissionDef(self, symbol: str, volume: float):
        return await self._transaction({
            "command": "getCommissionDef",
            "arguments": {
                "symbol": symbol,
                "volume": volume
            }
        })

    async def getCurrentUserData(self):
        return await self._transaction({
            "command": "getCurrentUserData"
        })

    async def getIbsHistory(self, start: int, end: int):
        return await self._transaction({
            "command": "getIbsHistory",
            "arguments": {
                "end": end,
                "start": start
            }
        })

    async def getMarginLevel(self):
        return await self._transaction({
            "command": "getMarginLevel"
        })

    async def getMarginTrade(self, symbol: str, volume: float):
        return await self._transaction({
            "command": "getMarginTrade",
            "arguments": {
                "symbol": symbol,
                "volume": volume
            }
        })

    async def getNews(self, start: int, end: int):
        return await self._transaction({
            "command": "getNews",
            "arguments": {
                "end": end,
                "start": start
            }
        })

    async def getProfitCalculation(self, symbol: str, cmd: int, openPrice: float, closePrice: float, volume: float):
        return await self._transaction({
            "command": "getProfitCalculation",
            "arguments": {
                "closePrice": closePrice,
                "cmd": cmd,
                "openPrice": openPrice,
                "symbol": symbol,
                "volume": volume
            }
        })

    async def getServerTime(self):
        return await self._transaction({
            "command": "getServerTime"
        })

    async def getStepRules(self):
        return await self._transaction({
            "command": "getStepRules"
        })

    async def getSymbol(self, symbol: str):
        return await self._transaction({
            "command": "getSymbol",
            "arguments": {
                "symbol": symbol
            }
        })

    async def getTickPrices(self, symbols: List[str], timestamp: int, level: int = 0 ):
        return await self._transaction({
            "command": "getTickPrices",
            "arguments": {
                "level": level,
                "symbols": symbols,
                "timestamp": timestamp
            }
        })

    async def getTradeRecords(self, orders: List[int]):
        return await self._transaction({
            "command": "getTradeRecords",
            "arguments": {
                "orders": orders
            }
        })

    async def getTrades(self, openedOnly: bool = True):
        return await self._transaction({
            "command": "getTrades",
            "arguments": {
                "openedOnly": openedOnly
            }
        })

    async def getTradesHistory(self, start: int, end: int = 0):
        return await self._transaction({
            "command": "getTradesHistory",
            "arguments": {
                "end": end,
                "start": start
            }
        })

    async def getTradingHours(self, symbols: List[str]):
        return await self._transaction({
            "command": "getTradingHours",
            "arguments": {
                "symbols": symbols
            }
        })

    async def getVersion(self):
        return await self._transaction({
            "command": "getVersion"
        })

    async def ping(self):
        return await self._transaction({
            "command": "ping"
        })

    async def tradeTransaction(self, symbol: str, cmd: TradeCmd, type: TradeType, price: float, volume: float,
                               sl: float = 0, tp: float = 0, order: int = 0, expiration: int = 0,
                               offset: int = 0, customComment: str = str()):
        if self.safe == True:
            return {
                "status": False,
                'errorCode': 'N/A',
                'errorDescr': 'Trading is disabled when safe=True'
            }

        return await self._transaction({
            "command": "tradeTransaction",
            "arguments": {
                "tradeTransInfo": {
                    "cmd": cmd.value,
                    "customComment": customComment,
                    "expiration": expiration,
                    "offset": offset,
                    "order": order,
                    "price": price,
                    "sl": sl,
                    "symbol": symbol,
                    "tp":   tp,
                    "type": type.value,
                    "volume": volume
                }
            }
        })

    async def tradeTransactionStatus(self, order: int):
        return await self._transaction({
            "command": "tradeTransactionStatus",
            "arguments": {
                "order": order
            }
        })
