import logging
import asyncio
import json
import xapi

logging.basicConfig(level=logging.INFO)

with open("credentials.json", "r") as f:
    CREDENTIALS = json.load(f)

# start from the first day of a current year
from datetime import datetime as dt
START = round(dt.today().replace(month=1, day=1).timestamp() * 1000)

async def main():
    try:
        async with await xapi.connect(**CREDENTIALS) as x:
            response = await x.socket.getTradesHistory(START)
            if response['status'] == True:
                print(response['returnData'])
            else:
                print("Failed to get trades history", response)

    except xapi.LoginFailed as e:
        print(f"Log in failed: {e}")

    except xapi.ConnectionClosed as e:
        print(f"Connection closed: {e}")

if __name__ == "__main__":
    asyncio.run(main())