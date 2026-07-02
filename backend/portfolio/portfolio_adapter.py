from datetime import datetime


class PortfolioAdapter:
    """
    Central account data gateway.

    Today:
        - Simulation

    Future:
        - Webull
        - Interactive Brokers
        - Tradier
        - Alpaca
    """

    def __init__(self):
        self.provider = "SIMULATION"

    def snapshot(self):

        return {

            "cash": 25000.00,
            "equity": 25340.82,
            "buying_power": 50000.00,

            "daily_pnl": 315.42,
            "unrealized_pnl": 142.80,
            "realized_pnl": 172.62,

            "open_positions": 2,
            "risk_used_pct": 1.8,

            "provider": self.provider,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


if __name__ == "__main__":

    adapter = PortfolioAdapter()

    portfolio = adapter.snapshot()

    print()
    print("==============================")
    print(" STRATPILOT PORTFOLIO ADAPTER")
    print("==============================")
    print()

    for key, value in portfolio.items():
        print(f"{key:18}: {value}")

    print()
    print("Portfolio snapshot ready.")
