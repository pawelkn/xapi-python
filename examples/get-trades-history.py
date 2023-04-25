from datetime import datetime as dt

import asyncio
import json
import xapi

with open("credentials.json", "r") as f:
    credentials = json.load(f)

async def main():
    try:
        x = await xapi.connect(**credentials)

        # start from the first day of a current year
        start = round(dt.today().replace(month=1, day=1).timestamp() * 1000)

        response = await x.socket.getTradesHistory(start)
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