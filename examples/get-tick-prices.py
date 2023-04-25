import asyncio
import json
import xapi

with open("credentials.json", "r") as f:
    credentials = json.load(f)

async def main():
    while True:
        try:
            x = await xapi.connect(**credentials)

            await x.stream.getTickPrices("BITCOIN")
            await x.stream.getTickPrices("ETHEREUM")

            async for message in x.stream.listen():
                print(message['data'])

        except xapi.LoginFailed as e:
            print(f"Log in failed: {e}")
            return

        except xapi.ConnectionClosed as e:
            print(f"Connection closed: {e}, reconnecting ...")
            continue

if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        pass