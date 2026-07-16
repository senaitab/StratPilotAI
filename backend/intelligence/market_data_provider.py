from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo


@dataclass
class MarketData:

    symbol: str

    price: float

    open_price: float

    high: float

    low: float

    previous_close: float

    volume: int

    timestamp: str


class MarketDataProvider:
    """
    Stage 30.0

    Central provider for market data.

    Placeholder values are used for now.
    Live Webull integration will replace these
    in future stages.
    """

    def get_market_data(
        self,
        symbol: str = "SPY",
    ) -> MarketData:

        eastern = ZoneInfo("America/New_York")

        now = datetime.now(eastern)

        return MarketData(
            symbol=symbol,
            price=734.82,
            open_price=733.60,
            high=735.20,
            low=732.95,
            previous_close=731.44,
            volume=185_000_000,
            timestamp=now.strftime("%Y-%m-%d %H:%M:%S"),
        )


if __name__ == "__main__":

    provider = MarketDataProvider()

    market = provider.get_market_data()

    print("\n===================================")
    print(" STRATPILOT MARKET DATA PROVIDER ")
    print("===================================")

    print(f"Symbol          : {market.symbol}")
    print(f"Price           : ${market.price:.2f}")
    print(f"Open            : ${market.open_price:.2f}")
    print(f"High            : ${market.high:.2f}")
    print(f"Low             : ${market.low:.2f}")
    print(f"Previous Close  : ${market.previous_close:.2f}")
    print(f"Volume          : {market.volume:,}")
    print(f"Timestamp       : {market.timestamp}")

    print("\nThink First. Trade Second.")
