# xStation5 API Python Library

[![Test xapi-python](https://github.com/pawelkn/xapi-python/actions/workflows/test-xapi-python.yml/badge.svg)](https://github.com/pawelkn/xapi-python/actions/workflows/test-xapi-python.yml) [![PyPi](https://img.shields.io/pypi/v/xapi-python.svg)](https://pypi.python.org/pypi/xapi-python/) [![Downloads](https://img.shields.io/pypi/dm/xapi-python)](https://pypi.python.org/pypi/xapi-python/) [![Codecov](https://codecov.io/gh/pawelkn/xapi-python/branch/master/graph/badge.svg)](https://codecov.io/gh/pawelkn/xapi-python/)

The xStation5 API Python library provides a simple and easy-to-use API for interacting with the xStation5 trading platform. With this library, you can connect to the xStation5 platform, retrieve market data, and execute trades.

This library may be used for [BFB Capital](https://bfb.capital) and [XTB](https://www.xtb.com) xStation5 accounts.

API documentation: <http://developers.xstore.pro/documentation>

## Disclaimer

This xStation5 API Python library is not affiliated with, endorsed by, or in any way officially connected to the xStation5 trading platform or its parent company. The library is provided as-is and is not guaranteed to be suitable for any particular purpose. The use of this library is at your own risk, and the author(s) of this library will not be liable for any damages arising from the use or misuse of this library. Please refer to the license file for more information.

## Installation

You can install xAPI using pip. Simply run the following command:

```shell
pip install xapi-python
```

## Usage

To use xAPI, you will need to have an active account with the xStation5 trading platform. Once you have an account, you can use the xAPI library to connect to the platform and begin trading.

Here is an example of how to use the xAPI library to connect to the xStation5 platform:

```python
import asyncio
import xapi

# Replace these values with your own credentials
CREDENTIALS = {
    "accountId": "<your_client_id>",
    "password": "<your_password>",
    "host": "ws.xtb.com",
    "type": "real",
    "safe": True
}

async def main():
    try:
        # Create a new xAPI object and connect to the xStation5 platform
        async with await xapi.connect(**CREDENTIALS) as x:
            pass

    except xapi.LoginFailed as e:
        print(f"Log in failed: {e}")

    except xapi.ConnectionClosed as e:
        print(f"Connection closed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

Once you have connected to the platform, you can use the xAPI object to retrieve market data and execute trades.

Here is an example of how to subscribe to market data using the xAPI library:

```python
import asyncio
import xapi

# Replace these values with your own credentials
CREDENTIALS = {
    "accountId": "<your_client_id>",
    "password": "<your_password>",
    "host": "ws.xtb.com",
    "type": "real",
    "safe": True
}

async def main():
    while True:
        try:
            async with await xapi.connect(**CREDENTIALS) as x:
                # Subscribe for the current price of BITCOIN and ETHEREUM
                await x.stream.getTickPrices("BITCOIN")
                await x.stream.getTickPrices("ETHEREUM")

                # Listen for coming price ticks
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
```

And here is an example of how to execute a trade using the xAPI library:

```python
import asyncio
import xapi
from xapi import TradeCmd, TradeType, TradeStatus

# Replace these values with your own credentials
CREDENTIALS = {
    "accountId": "<your_client_id>",
    "password": "<your_password>",
    "host": "ws.xtb.com",
    "type": "real",
    "safe": False
}

async def main():
    try:
        async with await xapi.connect(**CREDENTIALS) as x:
            # Open a new trade for BITCOIN
            response = await x.socket.tradeTransaction(
                symbol="BITCOIN",
                cmd=TradeCmd.BUY_LIMIT,
                type=TradeType.OPEN,
                price=10.00,
                volume=1
            )

            if response['status'] == True:
                print("Transaction sent to market")
            else:
                print("Failed to trade a transaction", response)

    except xapi.LoginFailed as e:
        print(f"Log in failed: {e}")

    except xapi.ConnectionClosed as e:
        print(f"Connection closed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Examples

To run the examples for the xAPI library, you will need to have an account with the xStation5 trading platform.

Before running the examples, you should create a file called _credentials.json_ in the project directory. This file should contain your account credentials, like this:

### credentials.json

```json
{
    "accountId": "<your_client_id>",
    "password": "<your_password>",
    "host": "ws.xtb.com",
    "type": "real",
    "safe": false
}
```

Once you have created the _credentials.json_ file, you can run an example using the following command:

```shell
python3 examples/get-margin-level.py
```

## Unit Tests

This will run all of the unit tests in the tests directory:

```shell
git clone https://github.com/pawelkn/xapi-python.git
cd xapi-python
python3 -m unittest discover tests
```

## Buy Me A Coffee! ☕

If you find the project beneficial and would like to support me, please consider showing your appreciation by buying me a coffee on [Buy Me A Coffee](https://www.buymeacoffee.com/pawelkn) or [Buy Coffee Poland](https://buycoffee.to/pawelkn)
