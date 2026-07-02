from datetime import datetime


class MarketAdapter:
    """
    Central gateway for all market data.

    Today:
        - Returns placeholder data.

    Future:
        - Webull
        - Polygon
        - TradingView
        - AlphaVantage
        - Any additional providers
    """

    def __init__(self):
        self.provider = "SIMULATION"

    def snapshot(self):

        return {
            "symbol": "SPY",
            "price": 731.42,
            "change_pct": 0.63,
            "volume": 42500000,
            "vix": 15.82,
            "market_status": "OPEN",
            "provider": self.provider,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }


if __name__ == "__main__":

    adapter = MarketAdapter()

    market = adapter.snapshot()

    print()
    print("==============================")
    print(" STRATPILOT MARKET ADAPTER")
    print("==============================")
    print()

    for key, value in market.items():
        print(f"{key:15}: {value}")

    print()
    print("Market snapshot ready.")
