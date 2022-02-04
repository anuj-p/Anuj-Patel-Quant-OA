"""
This module contains classes and functions related to forex to be used
for strawberry schema.
"""

from polygon_client import forex as polygon_client
import strawberry


@strawberry.type
class Forex:
    @strawberry.field
    def foo(self) -> str:
        return "bar"
