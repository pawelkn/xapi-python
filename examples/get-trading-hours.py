import logging
import asyncio
import datetime
import time
import pytz
import json
import xapi

logging.basicConfig(level=logging.INFO)

with open("credentials.json", "r") as f:
    CREDENTIALS = json.load(f)

WARSAW_TZ = pytz.timezone("Europe/Warsaw")
LOCAL_TZ = pytz.timezone(time.tzname[0])

def format_time(ms):
    seconds = ms / 1000.0
    dt = datetime.datetime.utcfromtimestamp(seconds)
    warsaw_dt = WARSAW_TZ.localize(dt)
    localized_dt = warsaw_dt.astimezone(LOCAL_TZ)
    formatted_time = localized_dt.strftime('%H:%M')
    return formatted_time

def format_weekday(day):
    return ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][day-1]

async def main():
    try:
        async with await xapi.connect(**CREDENTIALS) as x:
            response = await x.socket.getTradingHours(["AAPL.US_9","BP.UK_9","PKO.PL_9","BITCOIN","EURUSD","US100"])
            if response['status'] == True:
                for data in response['returnData']:
                    print(f"Symbol: {data['symbol']}")
                    print(f"Trading hours (Local time):")
                    for d in sorted(data['trading'], key=lambda x: x['day']):
                        print(f"  {format_weekday(d['day'])}   {format_time(d['fromT'])} - {format_time(d['toT'])}")
                    print()
            else:
                print("Failed to get trading hours", response)

    except xapi.LoginFailed as e:
        print(f"Log in failed: {e}")

    except xapi.ConnectionClosed as e:
        print(f"Connection closed: {e}")

if __name__ == "__main__":
    asyncio.run(main())