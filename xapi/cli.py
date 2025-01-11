import xapi

import datetime
import logging
import asyncio
import click
import json
import csv
import sys
import os

class TradeCmdType(click.ParamType):
    name = "TRADE_CMD"

    def __init__(self):
        self.cmds = xapi.TradeCmd.__members__.keys()

    def convert(self, value, param, ctx):
        try:
            return xapi.TradeCmd[value.upper()]
        except KeyError:
            self.fail(f"{value} is not a valid trade command.\n" +
                f"Expected one of: [{', '.join(self.cmds)}]", param, ctx)

class TradeTypeType(click.ParamType):
    name = "TRADE_TYPE"

    def __init__(self):
        self.types = xapi.TradeType.__members__.keys()

    def convert(self, value, param, ctx):
        try:
            return xapi.TradeType[value.upper()]
        except KeyError:
            self.fail(f"{value} is not a valid trade type.\n" +
                f"Expected one of: [{', '.join(self.types)}]", param, ctx)

class PeriodCodeType(click.ParamType):
    name = "PERIOD_CODE"

    def __init__(self):
        self.codes = [key[7:] for key in xapi.PeriodCode.__members__.keys()] # trim "PERIOD_"

    def convert(self, value, param, ctx):
        try:
            return xapi.PeriodCode[f"PERIOD_{value.upper()}"]
        except KeyError:
            self.fail(f"{value} is not a valid period code.\n" +
                f"Expected one of: [{', '.join(self.codes)}]", param, ctx)

class DateTimeType(click.ParamType):
    name = 'DATETIME'

    def __init__(self):
        self.formats = [
            "<epoch timestamp>",
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M"
        ]

    def convert(self, value, param, ctx):
        try:
            value = float(value)
            if value < 1e10: # if value is in seconds
                value *= 1000
            return int(value)
        except ValueError:
            pass

        for format in self.formats[1:]:
            try:
                return int(datetime.datetime.strptime(value, format).timestamp() * 1000)
            except ValueError:
                pass

        self.fail(f"{value} is not a valid datetime.\n" +
            f"Expected one of: [{', '.join(self.formats)}]", param, ctx)

@click.group()
@click.option(
    "--credentials-file",
    "-c",
    default="",
    envvar="XAPI_CREDENTIALS_FILE",
    help="Path to XAPI credentials file. It can be provided in the XAPI_CREDENTIALS_FILE environment variable. " +
        "Default is local credentials.json or global ~/.xapi-python/credentials.json.",
)
@click.option("--account-id", "-a", help="XTB account id. Use to authenticate without a credentials file.")
@click.option("--password", "-p", help="Program will prompt for input if not provided.")
@click.option("--host", "-h", default="ws.xtb.com", help="XTB host. Default is: ws.xtb.com.")
@click.option("--type", "-t", default="real", help="Account type. Default is: real.")
@click.option("--safe", "-s", default=False, is_flag=True, help="Safe mode. Default is: false.")
@click.version_option(xapi.__version__)
@click.pass_context
def cli(ctx, credentials_file, account_id, password, host, type, safe):
    ctx.ensure_object(dict)

    def load(file):
        if os.path.exists(file):
            with open(file, "r") as f:
                return json.load(f)
        return None

    if account_id is None:
        credentials = load(credentials_file) or \
                      load(os.path.join(".", "credentials.json")) or \
                      load(os.path.join(os.path.expanduser("~"), ".xapi-python", "credentials.json"))

        if credentials:
            ctx.obj['credentials'] = credentials
            return

        account_id = click.prompt("Account ID")

    if password is None:
        password = click.prompt("Password", hide_input=True)

    ctx.obj['credentials'] = {
        "accountId": account_id,
        "password": password,
        "host": host,
        "type": type,
        "safe": safe
    }

def print_csv(arr):
    if not arr:
        return

    if not isinstance(arr, list):
        arr = [arr]

    if 'csv_writer' not in globals():
        global csv_writer
        csv_writer = csv.DictWriter(sys.stdout, fieldnames=arr[0].keys())
        csv_writer.writeheader()

    csv_writer.writerows(arr)

def run(ctx, **kwds):
    async def run():
        while True:
            try:
                async with await xapi.connect(**ctx.obj['credentials']) as x:
                    command = ctx.command.name
                    if command == "get-all-symbols":
                        result = await x.socket.getAllSymbols()
                    elif command == "get-calendar":
                        result = await x.socket.getCalendar()
                    elif command == "get-chart-last-request":
                        result = await x.socket.getChartLastRequest(kwds['symbol'], kwds['start'], kwds['period'])
                    elif command == "get-chart-range-request":
                        result = await x.socket.getChartRangeRequest(kwds['symbol'], kwds['start'], kwds['end'], kwds['period'], kwds['ticks'])
                    elif command == "get-commission-def":
                        result = await x.socket.getCommissionDef(kwds['symbol'], kwds['volume'])
                    elif command == "get-current-user-data":
                        result = await x.socket.getCurrentUserData()
                    elif command == "get-ibs-history":
                        result = await x.socket.getIbsHistory(kwds['start'], kwds['end'])
                    elif command == "get-margin-level":
                        result = await x.socket.getMarginLevel()
                    elif command == "get-margin-trade":
                        result = await x.socket.getMarginTrade(kwds['symbol'], kwds['volume'])
                    elif command == "get-news":
                        result = await x.socket.getNews(kwds['start'], kwds['end'])
                    elif command == "get-profit-calculation":
                        result = await x.socket.getProfitCalculation(kwds['symbol'], kwds['cmd'], kwds['volume'], kwds['open'], kwds['close'])
                    elif command == "get-server-time":
                        result = await x.socket.getServerTime()
                    elif command == "get-step-rules":
                        result = await x.socket.getStepRules()
                    elif command == "get-symbol":
                        result = await x.socket.getSymbol(kwds['symbol'])
                    elif command == "get-tick-prices":
                        result = await x.socket.getTickPrices(kwds['symbols'], kwds['timestamp'], kwds['level'])
                    elif command == "get-trade-records":
                        result = await x.socket.getTradeRecords(kwds['orders'])
                    elif command == "get-trades":
                        result = await x.socket.getTrades(kwds['opened_only'])
                    elif command == "get-trades-history":
                        result = await x.socket.getTradesHistory(kwds['start'], kwds['end'])
                    elif command == "get-trading-hours":
                        result = await x.socket.getTradingHours(kwds['symbols'])
                    elif command == "get-version":
                        result = await x.socket.getVersion()
                    elif command == "listen-balance":
                        await x.stream.getBalance()
                    elif command == "listen-candles":
                        await x.stream.getCandles(kwds['symbol'])
                    elif command == "listen-news":
                        await x.stream.getNews()
                    elif command == "listen-profits":
                        await x.stream.getProfits()
                    elif command == "listen-tick-prices":
                        await x.stream.getTickPrices(kwds['symbol'], kwds['min_arrival_time'], kwds['max_level'])
                    elif command == "listen-trades":
                        await x.stream.getTrades()
                    elif command == "listen-trade-status":
                        await x.stream.getTradeStatus()
                    elif command == "trade-transaction":
                        result = await x.socket.tradeTransaction(kwds['symbol'], kwds['cmd'], kwds['type'], kwds['price'], kwds['volume'],
                            kwds['sl'], kwds['tp'], kwds['order'], kwds['expiration'], kwds['offset'], kwds['custom_comment'])
                    else:
                        print(f"Unknown command: {command}", file=sys.stderr)
                        return

                    if command.startswith("listen"):
                        async for message in x.stream.listen():
                            if kwds.get("csv"):
                                print_csv(message.get('data'))
                            else:
                                print(json.dumps(message.get('data'), indent=None))

                    if result.get('status'):
                        returnData = result.get('returnData')
                        if returnData:
                            if kwds.get("csv"):
                                if command.startswith("get-chart"):
                                    print_csv(returnData.get('rateInfos'))
                                else:
                                    print_csv(returnData)
                            else:
                                print(json.dumps(returnData, indent=2))
                    else:
                        print(f"Failed: {result}", file=sys.stderr)
                    return

            except xapi.LoginFailed as e:
                print(f"Log in failed: {e}", file=sys.stderr)
                return

            except xapi.ConnectionClosed as e:
                print(f"Connection closed: {e}, reconnecting ...", file=sys.stderr)
                await asyncio.sleep(1)
                continue

    try:
        asyncio.run(run())

    except KeyboardInterrupt:
        pass

click.csv_option = click.option("--csv", default=False, help="Output in CSV format. Default is JSON.", is_flag=True)

@cli.command("get-all-symbols", short_help="Gets all symbols.")
@click.csv_option
@click.pass_context
def get_all_symbols(ctx, csv):
    """
    Gets all symbols.
    """
    run(ctx, csv=csv)

@cli.command("get-calendar", short_help="Gets the calendar information.")
@click.csv_option
@click.pass_context
def get_calendar(ctx, csv):
    """
    Gets the calendar information.
    """
    run(ctx, csv=csv)

@cli.command("get-chart-last-request", short_help="Gets the chart last request information.")
@click.argument("symbol")
@click.option("--start", type=DateTimeType(), default=0)
@click.option("--period", type=PeriodCodeType(), default="D1")
@click.csv_option
@click.pass_context
def get_chart_last_request(ctx, symbol, start, period, csv):
    """
    Gets the chart last request information.

    \b
    Arguments:
        SYMBOL: Symbol (e.g., EURUSD).
    """
    run(ctx, symbol=symbol, start=start, period=period, csv=csv)

@cli.command("get-chart-range-request", short_help="Gets the chart range request information.")
@click.argument("symbol")
@click.option("--start", type=DateTimeType(), default=0, help="Start time.")
@click.option("--end", type=DateTimeType(), default=0, help="End time.")
@click.option("--period", type=PeriodCodeType(), default="D1", help="Period code.")
@click.option("--ticks", type=int, default=0, help="Number of ticks.")
@click.csv_option
@click.pass_context
def get_chart_range_request(ctx, symbol, start, end, period, ticks, csv):
    """
    Gets the chart range request information.

    \b
    Arguments:
        SYMBOL: Symbol (e.g., EURUSD).
    """
    run(ctx, symbol=symbol, start=start, end=end, period=period, ticks=ticks, csv=csv)

@cli.command("get-commission-def", short_help="Gets the commission definition.")
@click.argument("symbol")
@click.option("--volume", type=float, default=0, help="Volume of the trade.")
@click.csv_option
@click.pass_context
def get_commission_def(ctx, symbol, volume, csv):
    """
    Gets the commission definition.

    \b
    Arguments:
        SYMBOL: Symbol (e.g., EURUSD).
    """
    run(ctx, symbol=symbol, volume=volume, csv=csv)

@cli.command("get-current-user-data", short_help="Gets the current user data.")
@click.csv_option
@click.pass_context
def get_current_user_data(ctx, csv):
    """
    Gets the current user data.
    """
    run(ctx, csv=csv)

@cli.command("get-ibs-history", short_help="Gets the IBS history.")
@click.option("--start", type=DateTimeType(), default=0, help="Start time.")
@click.option("--end", type=DateTimeType(), default=0, help="End time.")
@click.csv_option
@click.pass_context
def get_ibs_history(ctx, start, end, csv):
    """
    Gets the IBS history.
    """
    run(ctx, start=start, end=end, csv=csv)

@cli.command("get-margin-level", short_help="Gets the margin level.")
@click.csv_option
@click.pass_context
def get_margin_level(ctx, csv):
    """
    Gets the margin level.
    """
    run(ctx, csv=csv)

@cli.command("get-margin-trade", short_help="Gets the margin trade.")
@click.argument("symbol")
@click.option("--volume", type=float, default=0, help="Volume of the trade.")
@click.csv_option
@click.pass_context
def get_margin_trade(ctx, symbol, volume, csv):
    """
    Gets the margin trade.

    \b
    Arguments:
        SYMBOL: Symbol (e.g., EURUSD).
    """
    run(ctx, symbol=symbol, volume=volume, csv=csv)

@cli.command("get-news", short_help="Gets the news.")
@click.option("--start", type=DateTimeType(), default=0, help="Start time.")
@click.option("--end", type=DateTimeType(), default=0, help="End time.")
@click.csv_option
@click.pass_context
def get_news(ctx, start, end, csv):
    """
    Gets the news.
    """
    run(ctx, start=start, end=end, csv=csv)

@cli.command("get-profit-calculation", short_help="Gets the profit calculation.")
@click.argument("symbol")
@click.argument("cmd", type=TradeCmdType())
@click.option("--volume", type=float, default=0, help="Volume of the trade.")
@click.option("--open", type=float, default=0, help="Open price.")
@click.option("--close", type=float, default=0, help="Close price.")
@click.csv_option
@click.pass_context
def get_profit_calculation(ctx, symbol, cmd, volume, open, close, csv):
    """
    Gets the profit calculation.

    \b
    Arguments:
        SYMBOL: Symbol (e.g., EURUSD).
        CMD: Command (one of: BUY, SELL, BUY_LIMIT, SELL_LIMIT, BUY_STOP, SELL_STOP).
    """
    run(ctx, symbol=symbol, cmd=cmd, volume=volume, open=open, close=close, csv=csv)

@cli.command("get-server-time", short_help="Gets the server time.")
@click.csv_option
@click.pass_context
def get_server_time(ctx, csv):
    """
    Gets the server time.
    """
    run(ctx, csv=csv)

@cli.command("get-step-rules", short_help="Gets the step rules.")
@click.csv_option
@click.pass_context
def get_step_rules(ctx, csv):
    """
    Gets the step rules.
    """
    run(ctx, csv=csv)

@cli.command("get-symbol", short_help="Gets the symbol information.")
@click.argument("symbol")
@click.csv_option
@click.pass_context
def get_symbol(ctx, symbol, csv):
    """
    Gets the symbol information.

    \b
    Arguments:
        SYMBOL: Symbol (e.g., EURUSD).
    """
    run(ctx, symbol=symbol, csv=csv)

@cli.command("get-tick-prices", short_help="Gets the tick prices.")
@click.argument("symbols", nargs=-1)
@click.option("--timestamp", type=int, default=0, help="Timestamp.")
@click.option("--level", type=int, default=0, help="Level.")
@click.csv_option
@click.pass_context
def get_tick_prices(ctx, symbols, timestamp, level, csv):
    """
    Gets the tick prices.

    \b
    Arguments:
        SYMBOLS: List of symbols (e.g., EURUSD BITCOIN 11B.PL).
    """
    run(ctx, symbols=symbols, timestamp=timestamp, level=level, csv=csv)

@cli.command("get-trade-records", short_help="Gets the trade records.")
@click.argument("orders", nargs=-1, type=int)
@click.csv_option
@click.pass_context
def get_trade_records(ctx, orders, csv):
    """
    Gets the trade records.

    \b
    Arguments:
        ORDERS: List of order numbers (e.g., 123456 123457).
    """
    run(ctx, orders=orders, csv=csv)

@cli.command("get-trades", short_help="Gets the trades.")
@click.option("--opened-only", "-o", default=True, is_flag=True, help="Opened only.")
@click.csv_option
@click.pass_context
def get_trades(ctx, opened_only, csv):
    """
    Gets the trades.
    """
    run(ctx, opened_only=opened_only, csv=csv)

@cli.command("get-trades-history", short_help="Gets the trades history.")
@click.option("--start", type=DateTimeType(), default=0, help="Start time.")
@click.option("--end", type=DateTimeType(), default=0, help="End time.")
@click.csv_option
@click.pass_context
def get_trades_history(ctx, start, end, csv):
    """
    Gets the trades history.
    """
    run(ctx, start=start, end=end, csv=csv)

@cli.command("get-trading-hours", short_help="Gets the trading hours.")
@click.argument("symbols", nargs=-1)
@click.csv_option
@click.pass_context
def get_trading_hours(ctx, symbols, csv):
    """
    Gets the trading hours.

    \b
    Arguments:
        SYMBOLS: List of symbols (e.g., EURUSD BITCOIN 11B.PL).
    """
    run(ctx, symbols=symbols, csv=csv)

@cli.command("get-version", short_help="Gets the version.")
@click.csv_option
@click.pass_context
def get_version(ctx, csv):
    """
    Gets the version.
    """
    run(ctx, csv=csv)

@cli.command("listen-balance", short_help="Listen balance.")
@click.csv_option
@click.pass_context
def listen_balance(ctx, csv):
    """
    Listen balance.
    """
    run(ctx, csv=csv)

@cli.command("listen-candles", short_help="Listen candles.")
@click.argument("symbol")
@click.csv_option
@click.pass_context
def listen_candles(ctx, symbol, csv):
    """
    Listen candles.

    \b
    Arguments:
        SYMBOL: Symbol (e.g., EURUSD).
    """
    run(ctx, symbol=symbol, csv=csv)

@cli.command("listen-news", short_help="Listen news.")
@click.csv_option
@click.pass_context
def listen_news(ctx, csv):
    """
    Listen news.
    """
    run(ctx, csv=csv)

@cli.command("listen-profits", short_help="Listen profits.")
@click.csv_option
@click.pass_context
def listen_profits(ctx, csv):
    """
    Listen profits.
    """
    run(ctx, csv=csv)

@cli.command("listen-tick-prices", short_help="Listen tick prices.")
@click.argument("symbol")
@click.option("--min-arrival-time", type=int, default=0, help="Minimum arrival time.")
@click.option("--max-level", type=int, default=2, help="Maximum level. Default is 2.")
@click.csv_option
@click.pass_context
def listen_tick_prices(ctx, symbol, min_arrival_time, max_level, csv):
    """
    Listen tick prices.

    \b
    Arguments:
        SYMBOL: Symbol (e.g., EURUSD).
    """
    run(ctx, symbol=symbol, min_arrival_time=min_arrival_time, max_level=max_level, csv=csv)

@cli.command("listen-trades", short_help="Listen trades.")
@click.csv_option
@click.pass_context
def listen_trades(ctx, csv):
    """
    Listen trades.
    """
    run(ctx, csv=csv)

@cli.command("listen-trade-status", short_help="Listen trade status.")
@click.csv_option
@click.pass_context
def listen_trade_status(ctx, csv):
    """
    Listen trade status.
    """
    run(ctx, csv=csv)

@cli.command("trade-transaction", short_help="Trade transaction.")
@click.argument("symbol")
@click.argument("cmd", type=TradeCmdType())
@click.argument("type", type=TradeTypeType())
@click.option("--price", type=float, default=0, help="Price of the trade.")
@click.option("--volume", type=float, default=0, help="Volume of the trade.")
@click.option("--sl", type=float, default=0, help="Stop loss value.")
@click.option("--tp", type=float, default=0, help="Take profit value.")
@click.option("--order", type=int, default=0, help="Order number.")
@click.option("--expiration", type=DateTimeType(), default=0, help="Expiration date and time.")
@click.option("--offset", type=int, default=0, help="Offset value.")
@click.option("--custom-comment", default="", help="Custom comment for the trade.")
@click.csv_option
@click.pass_context
def trade_transaction(ctx, symbol, cmd, type, price, volume, sl, tp, order, expiration, offset, custom_comment, csv):
    """
    Trade transaction.

    \b
    Arguments:
        SYMBOL: Symbol (e.g., EURUSD).
        CMD: Command (one of: BUY, SELL, BUY_LIMIT, SELL_LIMIT, BUY_STOP, SELL_STOP).
        TYPE: Type (one of: OPEN, CLOSE, MODIFY, DELETE).

    \b
    Examples:
        xapi trade-transaction 4MS.PL BUY_LIMIT OPEN --price 1.12 --volume 1
        xapi trade-transaction 4MS.PL SELL_LIMIT OPEN --price 1.12 --volume 1
        xapi trade-transaction 4MS.PL SELL_LIMIT MODIFY --order 123456 --price 1.13 --volume 1
        xapi trade-transaction 4MS.PL SELL_LIMIT DELETE --order 123456
    """
    run(ctx, symbol=symbol, cmd=cmd, type=type, price=price, volume=volume, sl=sl, tp=tp, order=order,
        expiration=expiration, offset=offset, custom_comment=custom_comment, csv=csv)