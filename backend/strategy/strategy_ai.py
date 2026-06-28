from intelligence.market_ai import MarketAI


class StrategyAI:

    def __init__(self):
        self.market = MarketAI()

    def analyze(self):

        report = self.market.analyze()

        price = report["price"]
        open_price = report["open"]

        change = ((price - open_price) / open_price) * 100

        if change > 0.30:
            bias = "BULLISH"
            recommendation = "CALL"

        elif change < -0.30:
            bias = "BEARISH"
            recommendation = "PUT"

        else:
            bias = "NEUTRAL"
            recommendation = "WAIT"

        confidence = min(abs(change) * 120, 95)

        return {
            "price": price,
            "change": round(change, 2),
            "bias": bias,
            "recommendation": recommendation,
            "confidence": round(confidence, 1)
        }


if __name__ == "__main__":

    ai = StrategyAI()

    report = ai.analyze()

    print("\n==============================")
    print("   STRATPILOT STRATEGY AI")
    print("==============================")

    print(f"SPY Price      : {report['price']}")
    print(f"Change         : {report['change']}%")
    print(f"Bias           : {report['bias']}")
    print(f"Recommendation : {report['recommendation']}")
    print(f"Confidence     : {report['confidence']}%")

    print("==============================")
