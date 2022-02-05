"""
This module contains classes and methods related to crypto to be used
for strawberry schema.
"""

from datetime import datetime
from graphql_wrapper import structs
from polygon_client import crypto as polygon_client
import strawberry
from typing import List


# user visible
@strawberry.type
class Crypto:
    @strawberry.field
    def aggregates(self, currency_to: str, currency_from: str, timespan: structs.Timespan, from_: str, to: str, multiplier: int = 1, adjusted: bool = True, sort: structs.Sort = structs.Sort.ASCENDING, limit: int = 5000) -> List["structs.AggregatesBar"]:
        """
        :param currency_to: currency symbol to exchange to (case-sensitive)
        :param currency_from: currency symbol to exchange from (case-sensitive)
        :param timespan: type of time window ('MINUTE'/'HOUR'/'DAY'/'WEEK'/'MONTH'/'QUARTER'/'YEAR')
        :param from_: starting date of the aggregate time window (YYYY-MM-DD)
        :param to: ending date of the aggregate time window (YYYY-MM-DD)
        :param multiplier: size of the timespan multiplier
        :param adjusted: whether or not the results are adjusted
        :param sort: type of timestamp sorting ('ASCENDING' or 'DESCENDING')
        :param limit: maximum number of base aggregates queried to create the aggregate results (<= 50000)
        :return: aggregate bars for a stock over a given date range in custom time window sizes
        """

        data = polygon_client.get_aggregates(currency_from, currency_to, multiplier, timespan.value, from_, to, adjusted=adjusted, ascending=sort.value, limit=limit)
        results = data["results"]
        market = []
        for result in results:
            market.append(structs.AggregatesBar(
                close=result["c"],
                high=result["h"],
                low=result["l"],
                transactions=result["n"] if "n" in result else -1,  # value is -1 if unavailable
                open=result["o"],
                time=datetime.utcfromtimestamp(result["t"] / 1000),
                volume=result["v"],
                vw_price=result["vw"] if "vw" in result else -1  # value is -1 if unavailable
            ))
        return market

    @strawberry.field
    def daily_open_close(self, currency_to: str, currency_from: str, date: str, adjusted: bool = True) -> structs.CryptoDailyOpenClose:
        """
        :param currency_to: currency symbol to exchange to (case-sensitive)
        :param currency_from: currency symbol to exchange from (case-sensitive)
        :param date: date of the requested open/close (YYYY-MM-DD)
        :param adjusted: whether or not the results are adjusted for splits
        :return: open prices, close prices, afterhours prices, and more (see Polygon's API docs)
        """

        data = polygon_client.get_daily_open_close(currency_to, currency_from, date, adjusted=adjusted)
        print(data)
        closing_trades = []
        for trade in data["closingTrades"]:
            closing_trades.append(structs.CryptoDailyOpenCloseTrade(
                conditions=trade["c"],
                price=trade["p"],
                volume=trade["s"],
                time=datetime.utcfromtimestamp(trade["t"] / 1000),
                exchange_id=trade["x"]
            ))
        opening_trades = []
        for trade in data["openTrades"]:
            opening_trades.append(structs.CryptoDailyOpenCloseTrade(
                conditions=trade["c"],
                price=trade["p"],
                volume=trade["s"],
                time=datetime.utcfromtimestamp(trade["t"] / 1000),
                exchange_id=trade["x"]
            ))
        return structs.CryptoDailyOpenClose(
            close=data["close"],
            closing_trades=closing_trades,
            open=data["open"],
            opening_trades=opening_trades
        )

    @strawberry.field
    def grouped_daily(self, date: str, adjusted: bool = True) -> List["structs.GroupedDailyBar"]:
        """
        :param date: date of the requested grouped daily (YYYY-MM-DD)
        :param adjusted: whether or not the results are adjusted
        :return: open prices, high prices, low prices, close prices, and more for the entire stock market (see Polygon's API docs)
        """

        data = polygon_client.get_grouped_daily(date, adjusted=adjusted)
        results = data["results"]
        market = []
        for result in results:
            market.append(structs.GroupedDailyBar(
                ticker=result["T"][2:] if result["T"][:2] == "X:" else result["T"],
                close=result["c"],
                high=result["h"],
                low=result["l"],
                transactions=result["n"] if "n" in result else -1,  # value is -1 if unavailable
                open=result["o"],
                time=datetime.utcfromtimestamp(result["t"] / 1000),
                volume=result["v"],
                vw_price=result["vw"] if "vw" in result else -1  # value is -1 if unavailable
            ))
        return market

    @strawberry.field
    def previous_close(self, currency_to: str, currency_from: str, adjusted: bool = True) -> structs.PreviousClose:
        """
        :param currency_to: currency symbol to exchange to (case-sensitive)
        :param currency_from: currency symbol to exchange from (case-sensitive)
        :param adjusted: whether or not the results are adjusted
        :return: previous day's open prices, high prices, low prices, close prices, and more (see Polygon's API docs)
        """

        data = polygon_client.get_previous_close(currency_to, currency_from, adjusted=adjusted)
        results = data["results"]
        result = results[0]
        return structs.PreviousClose(
            ticker=result["T"],
            close=result["c"],
            high=result["h"],
            low=result["l"],
            transactions=result["n"] if "n" in result else -1,  # value is -1 if unavailable
            open=result["o"],
            time=datetime.utcfromtimestamp(result["t"] / 1000),
            volume=result["v"],
            vw_price=result["vw"] if "vw" in result else -1  # value is -1 if unavailable
        )
