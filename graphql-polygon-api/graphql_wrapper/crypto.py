"""
This module contains classes and functions related to crypto to be used
for strawberry schema.
"""

from polygon_client import crypto as polygon_client
import strawberry


@strawberry.type
class Crypto:
    @strawberry.field
    def foo(self) -> str:
        return "bar"
