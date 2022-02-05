"""
This module contains classes and methods related to stocks to be used
for strawberry schema.
"""

from datetime import datetime
from enum import Enum
from polygon_client import stocks as polygon_client
import strawberry
from typing import List


# enums
@strawberry.enum
class AggregatesTimespan(Enum):
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"


@strawberry.enum
class AggregatesSort(Enum):
    ASCENDING = True
    DESCENDING = False


# output structures
@strawberry.type
class AggregatesBar:
    close: float
    high: float
    low: float
    transactions: float
    open: float
    time: datetime
    volume: float  # apparently volume can be non-integer...
    vw_price: float


@strawberry.type
class DailyOpenClose:
    after_hours: float
    close: float
    high: float
    low: float
    open: float
    pre_market: float
    volume: int


@strawberry.type
class GroupedDailyBar:
    ticker: str
    close: float
    high: float
    low: float
    transactions: float
    open: float
    time: datetime
    volume: float  # apparently volume can be non-integer...
    vw_price: float


@strawberry.type
class PreviousClose:
    close: float
    high: float
    low: float
    transactions: float
    open: float
    time: datetime
    volume: float  # apparently volume can be non-integer...
    vw_price: float


# user visible
@strawberry.type
class Stocks:
    @strawberry.field
    def aggregates(self, ticker: str, timespan: AggregatesTimespan, from_: str, to: str, multiplier: int = 1, adjusted: bool = True, sort: AggregatesSort = AggregatesSort.ASCENDING, limit: int = 5000) -> List["AggregatesBar"]:
        """
        :param ticker: ticker symbol of the stock (case-sensitive)
        :param multiplier: size of the timespan multiplier
        :param timespan: type of time window ('MINUTE'/'HOUR'/'DAY'/'WEEK'/'MONTH'/'QUARTER'/'YEAR')
        :param from_: starting date of the aggregate time window (YYYY-MM-DD)
        :param to: ending date of the aggregate time window (YYYY-MM-DD)
        :param adjusted: whether or not the results are adjusted for splits
        :param sort: type of timestamp sorting ('ASCENDING' or 'DESCENDING')
        :param limit: maximum number of base aggregates queried to create the aggregate results (<= 50000)
        :return: aggregate bars for a stock over a given date range in custom time window sizes
        """

        data = polygon_client.get_aggregates(ticker, multiplier, timespan.value, from_, to, adjusted=adjusted, ascending=sort.value, limit=limit)
        results = data["results"]
        market = []
        for result in results:
            market.append(AggregatesBar(
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
    def daily_open_close(self, ticker: str, date: str, adjusted: bool = True) -> DailyOpenClose:
        """
        :param ticker: ticker symbol of the stock (case-sensitive)
        :param date: date of the requested open/close (YYYY-MM-DD)
        :param adjusted: whether or not the results are adjusted for splits
        :return: open prices, close prices, afterhours prices, and more (see Polygon's API docs)
        """

        data = polygon_client.get_daily_open_close(ticker, date, adjusted=adjusted)
        return DailyOpenClose(
            after_hours=data["afterHours"],
            close=data["close"],
            high=data["high"],
            low=data["low"],
            open=data["open"],
            pre_market=data["preMarket"],
            volume=data["volume"],
        )

    @strawberry.field
    def grouped_daily(self, date: str, adjusted: bool = True) -> List["GroupedDailyBar"]:
        """
        :param date: date of the requested grouped daily (YYYY-MM-DD)
        :param adjusted: whether or not the results are adjusted for splits
        :return: open prices, high prices, low prices, close prices, and more for the entire stock market (see Polygon's API docs)
        """

        data = polygon_client.get_grouped_daily(date, adjusted=adjusted)
        results = data["results"]
        market = []
        for result in results:
            market.append(GroupedDailyBar(
                ticker=result["T"],
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
    def previous_close(self, ticker: str, adjusted: bool = True) -> PreviousClose:
        """
        :param ticker: ticker symbol of the stock (case-sensitive)
        :param adjusted: whether or not the results are adjusted for splits
        :return: previous day's open prices, high prices, low prices, close prices, and more (see Polygon's API docs)
        """

        data = polygon_client.get_previous_close(ticker, adjusted=adjusted)
        results = data["results"]
        result = results[0]
        return PreviousClose(
            close=result["c"],
            high=result["h"],
            low=result["l"],
            transactions=result["n"] if "n" in result else -1,  # value is -1 if unavailable
            open=result["o"],
            time=datetime.utcfromtimestamp(result["t"] / 1000),
            volume=result["v"],
            vw_price=result["vw"] if "vw" in result else -1  # value is -1 if unavailable
        )