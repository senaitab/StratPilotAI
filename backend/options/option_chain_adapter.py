from datetime import datetime


class OptionChainAdapter:
    """
    Central option chain gateway.

    Current:
        Simulation

    Future:
        Webull
        Tradier
        Polygon
        Interactive Brokers
    """

    def __init__(self):
        self.provider = "SIMULATION"

    def snapshot(self):

        return {

            "symbol": "SPY",

            "expiration": "2026-07-02",

            "strike": 732,

            "type": "CALL",

            "bid": 5.18,

            "ask": 5.24,

            "last": 5.20,

            "volume": 18245,

            "open_interest": 40218,

            "iv": 18.7,

            "delta": 0.54,

            "gamma": 0.081,

            "theta": -0.23,

            "vega": 0.12,

            "provider": self.provider,

            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        }


if __name__ == "__main__":

    adapter = OptionChainAdapter()

    option = adapter.snapshot()

    print()
    print("==============================")
    print(" STRATPILOT OPTION ADAPTER")
    print("==============================")
    print()

    for key, value in option.items():
        print(f"{key:18}: {value}")

    print()
    print("Option chain snapshot ready.")
