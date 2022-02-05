from graphql_wrapper import stocks
from graphql_wrapper import options
from graphql_wrapper import forex
from graphql_wrapper import crypto
from graphql_wrapper import futures
import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def stocks(self) -> stocks.Stocks:
        return stocks.Stocks()

    @strawberry.field
    def options(self) -> options.Options:
        return options.Options()

    @strawberry.field
    def forex(self) -> forex.Forex:
        return forex.Forex()

    @strawberry.field
    def crypto(self) -> crypto.Crypto:
        return crypto.Crypto()

    @strawberry.field
    def futures(self) -> futures.Futures:
        return futures.Futures()


schema = strawberry.Schema(query=Query)
