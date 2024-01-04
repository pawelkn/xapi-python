import logging
import asyncio
import json
import xapi

logging.basicConfig(level=logging.INFO)

with open("credentials.json", "r") as f:
    CREDENTIALS = json.load(f)

async def main():
    while True:
        try:
            async with await xapi.connect(**CREDENTIALS) as x:
                await x.stream.getProfits()

                async for message in x.stream.listen():
                    print(message['data'])

        except xapi.LoginFailed as e:
            print(f"Log in failed: {e}")
            return

        except xapi.ConnectionClosed as e:
            print(f"Connection closed: {e}, reconnecting ...")
            await asyncio.sleep(1)
            continue

if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        pass