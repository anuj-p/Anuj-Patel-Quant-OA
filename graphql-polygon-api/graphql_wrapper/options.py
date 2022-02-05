"""
This module contains classes and methods related to options to be used
for strawberry schema.
"""

from datetime import datetime
from graphql_wrapper import structs
from polygon_client import options as polygon_client
import strawberry
from typing import List


# user visible
@strawberry.type
class Options:
    @strawberry.field
    def aggregates(self, ticker: str, expiration: str, type: structs.OptionsType, strike: float, timespan: structs.Timespan, from_: str, to: str, multiplier: int = 1, adjusted: bool = True, sort: structs.Sort = structs.Sort.ASCENDING, limit: int = 5000) -> List["structs.AggregatesBar"]:
        """
        :param ticker: ticker symbol of the underlying stock
        :param expiration: expiration date of the option (YYYY-MM-DD)
        :param type: type of option ('CALL' or 'PUT')
        :param strike: strike price of the option
        :param timespan: type of time window ('MINUTE'/'HOUR'/'DAY'/'WEEK'/'MONTH'/'QUARTER'/'YEAR')
        :param from_: starting date of the aggregate time window (YYYY-MM-DD)
        :param to: ending date of the aggregate time window (YYYY-MM-DD)
        :param multiplier: size of the timespan multiplier
        :param adjusted: whether or not the results are adjusted for splits
        :param sort: type of timestamp sorting ('ASCENDING' or 'DESCENDING')
        :param limit: maximum number of base aggregates queried to create the aggregate results (<= 50000)
        :return: aggregate bars for an option over a given date range in custom time window sizes
        """

        data = polygon_client.get_aggregates(ticker, expiration, type.value, strike, multiplier, timespan.value, from_, to, adjusted=adjusted, ascending=sort.value, limit=limit)
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
    def daily_open_close(self, ticker: str, expiration: str, type: structs.OptionsType, strike: float, date: str, adjusted: bool = True) -> structs.DailyOpenClose:
        """
        :param ticker: ticker symbol of the underlying stock
        :param expiration: expiration date of the option (YYYY-MM-DD)
        :param type: type of option ('CALL' or 'PUT')
        :param strike: strike price of the option
        :param date: date of the requested open/close (YYYY-MM-DD)
        :param adjusted: whether or not the results are adjusted for splits
        :return: open prices, close prices, afterhours prices, and more (see Polygon's API docs)
        """

        data = polygon_client.get_daily_open_close(ticker, expiration, type.value, strike, date, adjusted=adjusted)
        return structs.DailyOpenClose(
            after_hours=data["afterHours"],
            close=data["close"],
            high=data["high"],
            low=data["low"],
            open=data["open"],
            pre_market=data["preMarket"],
            volume=data["volume"],
        )

    @strawberry.field
    def previous_close(self, ticker: str, expiration: str, type: structs.OptionsType, strike: float, adjusted: bool = True) -> structs.PreviousClose:
        """
        :param ticker: ticker symbol of the underlying stock
        :param expiration: expiration date of the option (YYYY-MM-DD)
        :param type: type of option ('CALL' or 'PUT')
        :param strike: strike price of the option
        :param adjusted: whether or not the results are adjusted for splits
        :return: previous day's open prices, high prices, low prices, close prices, and more (see Polygon's API docs)
        """

        data = polygon_client.get_previous_close(ticker, expiration, type.value, strike, adjusted=adjusted)
        results = data["results"]
        result = results[0]
        return structs.PreviousClose(
            close=result["c"],
            high=result["h"],
            low=result["l"],
            transactions=result["n"] if "n" in result else -1,  # value is -1 if unavailable
            open=result["o"],
            time=datetime.utcfromtimestamp(result["t"] / 1000),
            volume=result["v"],
            vw_price=result["vw"] if "vw" in result else -1  # value is -1 if unavailable
        )
