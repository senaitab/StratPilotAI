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

        if change_pct >= 1.0:
            bias = "STRONG BULLISH"
            recommendation = "LOOK FOR CALLS"
            confidence = 90

        elif change_pct >= 0.30:
            bias = "BULLISH"
            recommendation = "CALLS FAVORABLE"
            confidence = 75

        elif change_pct <= -1.0:
            bias = "STRONG BEARISH"
            recommendation = "LOOK FOR PUTS"
            confidence = 90

        elif change_pct <= -0.30:
            bias = "BEARISH"
            recommendation = "PUTS FAVORABLE"
            confidence = 75

        else:
            bias = "NEUTRAL"
            recommendation = "WAIT"
            confidence = 40

        return {
            "session": self.status.session(),
            "price": last,
            "open": open_price,
            "change_pct": round(change_pct, 2),
            "bias": bias,
            "recommendation": recommendation,
            "confidence": confidence,
        }


if __name__ == "__main__":
    ai = MarketAI()
    report = ai.analyze()

    print("\n===================================")
    print("     STRATPILOT AI REPORT")
    print("===================================")
    print(f"Session        : {report['session']}")
    print(f"SPY Price      : {report['price']:.2f}")
    print(f"Open           : {report['open']:.2f}")
    print(f"Change         : {report['change_pct']}%")
    print(f"Bias           : {report['bias']}")
    print(f"Recommendation : {report['recommendation']}")
    print(f"Confidence     : {report['confidence']}%")
    print("===================================")
