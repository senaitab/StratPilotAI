from market.market_status import MarketStatus
from market.quotes import QuoteEngine


class MarketAI:
    def __init__(self):
        self.status = MarketStatus()
        self.quote_engine = QuoteEngine()

    def analyze(self):
        spy = self.quote_engine.quote("SPY")[0]

        last = float(spy["price"])
        open_price = float(spy["open"])

        change_pct = ((last - open_price) / open_price) * 100

        if change_pct > 0.5:
            bias = "BULLISH"
        elif change_pct < -0.5:
            bias = "BEARISH"
        else:
            bias = "NEUTRAL"

        return {
            "session": self.status.session(),
            "price": last,
            "change_pct": round(change_pct, 2),
            "bias": bias,
        }


if __name__ == "__main__":
    ai = MarketAI()
    report = ai.analyze()

    print("\n==============================")
    print(" STRATPILOT AI MARKET REPORT")
    print("==============================")
    print(f"Session : {report['session']}")
    print(f"SPY     : {report['price']}")
    print(f"Change  : {report['change_pct']}%")
    print(f"Bias    : {report['bias']}")
    print("==============================")
