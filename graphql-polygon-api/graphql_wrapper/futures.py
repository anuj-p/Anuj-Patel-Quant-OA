"""
This module acts as an EXAMPLE and would contain classes and functions
related to futures to be used for strawberry schema.
"""

import strawberry


@strawberry.type
class Futures:
    @strawberry.field
    def foo(self) -> str:
        return "bar"
