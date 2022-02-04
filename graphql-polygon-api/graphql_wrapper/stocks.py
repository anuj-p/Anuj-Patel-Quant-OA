"""
This module contains classes and functions related to stocks to be used
for strawberry schema.
"""

from polygon_client import stocks as polygon_client
import strawberry


@strawberry.type
class Stocks:
    @strawberry.field
    def foo(self) -> str:
        return "bar"
