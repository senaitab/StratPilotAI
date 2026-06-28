from intelligence.market_ai import MarketAI
from risk.risk_ai import RiskAI


class DataCacheAI:
    def __init__(self):
        self.market_ai = MarketAI()
        self.risk_ai = RiskAI()

    def snapshot(self):
        market = self.market_ai.analyze()
        risk = self.risk_ai.analyze()

        return {
            "market": market,
            "risk": risk,
        }


if __name__ == "__main__":
    cache = DataCacheAI()
    data = cache.snapshot()

    print("\n===================================")
    print("        STRATPILOT DATA CACHE")
    print("===================================")
    print(f"Market Session : {data['market']['session']}")
    print(f"SPY Price      : {data['market']['price']}")
    print(f"Market Bias    : {data['market']['bias']}")
    print(f"Risk Status    : {data['risk']['status']}")
    print(f"Account Size   : ${data['risk']['account_size']:.2f}")
    print("===================================")
    print("Think First. Trade Second.")
