from dataclasses import dataclass


@dataclass
class MarketConfidence:
    market: int
    trend: int
    volatility: int
    liquidity: int
    session: int
    overall: int
    confidence: str
    recommendation: str


class MarketConfidenceEngine:

    def calculate(
        self,
        market_score: int,
        trend_score: int,
        volatility_score: int,
        liquidity_score: int,
        session_score: int,
    ) -> MarketConfidence:

        overall = round(
            (
                market_score
                + trend_score
                + volatility_score
                + liquidity_score
                + session_score
            )
            / 5
        )

        if overall >= 90:
            confidence = "VERY HIGH"
            recommendation = "STRONG TRADE"

        elif overall >= 80:
            confidence = "HIGH"
            recommendation = "TRADE"

        elif overall >= 65:
            confidence = "MEDIUM"
            recommendation = "CAUTION"

        else:
            confidence = "LOW"
            recommendation = "WAIT"

        return MarketConfidence(
            market_score,
            trend_score,
            volatility_score,
            liquidity_score,
            session_score,
            overall,
            confidence,
            recommendation,
        )


if __name__ == "__main__":

    engine = MarketConfidenceEngine()

    result = engine.calculate(
        market_score=100,
        trend_score=92,
        volatility_score=81,
        liquidity_score=94,
        session_score=25,
    )

    print("\n===================================")
    print("STRATPILOT MARKET CONFIDENCE")
    print("===================================")

    print(f"Market Context : {result.market}")
    print(f"Trend          : {result.trend}")
    print(f"Volatility     : {result.volatility}")
    print(f"Liquidity      : {result.liquidity}")
    print(f"Session        : {result.session}")

    print("-----------------------------------")

    print(f"Overall Score  : {result.overall}/100")
    print(f"Confidence     : {result.confidence}")

    print(f"\nRecommendation : {result.recommendation}")

    print("\nThink First. Trade Second.")
