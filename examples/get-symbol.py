import asyncio
import json
import xapi

with open("credentials.json", "r") as f:
    credentials = json.load(f)

async def main():
    try:
        x = await xapi.connect(**credentials)

        response = await x.socket.getSymbol("BITCOIN")
        if response['status'] == True:
            print(response['returnData'])
        else:
            print("Failed to get symbol", response)

    except xapi.LoginFailed as e:
        print(f"Log in failed: {e}")

    except xapi.ConnectionClosed as e:
        print(f"Connection closed: {e}")

if __name__ == "__main__":
    asyncio.run(main())