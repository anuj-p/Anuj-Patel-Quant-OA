from datetime import datetime
from enum import Enum
import strawberry
from typing import List


# enums
@strawberry.enum
class OptionsType(Enum):
    CALL = True
    PUT = False


@strawberry.enum
class Timespan(Enum):
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"


@strawberry.enum
class Sort(Enum):
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
    volume: float
    vw_price: float


@strawberry.type
class CryptoDailyOpenCloseTrade:
    conditions: List[int]
    price: float
    volume: float
    time: datetime
    exchange_id: strawberry.ID


@strawberry.type
class CryptoDailyOpenClose:
    close: float
    closing_trades: List[CryptoDailyOpenCloseTrade]
    open: float
    opening_trades: List[CryptoDailyOpenCloseTrade]


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
    volume: float
    vw_price: float


@strawberry.type
class PreviousClose:
    close: float
    high: float
    low: float
    transactions: float
    open: float
    time: datetime
    volume: float
    vw_price: float
