"""
This module contains classes and functions related to options to be used
for strawberry schema.
"""

from polygon_client import options as polygon_client
import strawberry


@strawberry.type
class Options:
    @strawberry.field
    def foo(self) -> str:
        return "bar"
