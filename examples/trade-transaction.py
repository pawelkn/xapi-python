import logging
import asyncio
import json
import xapi
from xapi import TradeCmd, TradeType, TradeStatus

logging.basicConfig(level=logging.INFO)

with open("credentials.json", "r") as f:
    CREDENTIALS = json.load(f)

async def main():
    try:
        async with await xapi.connect(**CREDENTIALS) as x:
            response = await x.socket.tradeTransaction(
                symbol="BITCOIN",
                cmd=TradeCmd.BUY_LIMIT,
                type=TradeType.OPEN,
                price=10.00,
                volume=1
            )

            if response['status'] != True:
                print("Failed to trade a transaction", response)
                return

            order = response['returnData']['order']

            response = await x.socket.tradeTransactionStatus(order)
            if response['status'] != True:
                print("Failed to trade a transaction", response)
                return

            requestStatus = response['returnData']['requestStatus']
            if requestStatus == TradeStatus.ERROR.value:
                print(f"The transaction finished with error: {response['returnData']['message']}")
            elif requestStatus == TradeStatus.PENDING.value:
                print(f"The transaction is pending")
            elif requestStatus == TradeStatus.ACCEPTED.value:
                print(f"The transaction has been executed successfully")
            elif requestStatus == TradeStatus.REJECTED.value:
                print(f"The transaction has been rejected: {response['returnData']['message']}")

    except xapi.LoginFailed as e:
        print(f"Log in failed: {e}")

    except xapi.ConnectionClosed as e:
        print(f"Connection closed: {e}")

if __name__ == "__main__":
    asyncio.run(main())