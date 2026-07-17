from dataclasses import dataclass
from datetime import time

from intelligence.market_data_provider import (
    MarketData,
    MarketDataProvider,
)


@dataclass
class SessionAnalysis:
    score: int
    session: str
    confidence: str
    explanation: str


class SessionAnalyzer:
    """
    Stage 30.4

    Determines trading session characteristics
    from the shared MarketData timestamp.

    Future versions will support:
    - Exchange holidays
    - Half trading days
    - Futures sessions
    - International exchanges
    """

    def analyze(self, market: MarketData) -> SessionAnalysis:

        current = market.timestamp.time()

        score = 50

        if time(9, 30) <= current < time(10, 30):
            session = "OPENING HOUR"
            score = 95

        elif time(10, 30) <= current < time(14, 0):
            session = "MIDDAY"
            score = 75

        elif time(14, 0) <= current < time(15, 30):
            session = "AFTERNOON"
            score = 85

        elif time(15, 30) <= current <= time(16, 0):
            session = "POWER HOUR"
            score = 100

        elif current < time(9, 30):
            session = "PRE-MARKET"
            score = 55

        else:
            session = "AFTER HOURS"
            score = 45

        if score >= 90:
            confidence = "VERY HIGH"
        elif score >= 75:
            confidence = "HIGH"
        elif score >= 60:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        explanation = (
            f"Current session is {session}. "
            f"Session score is {score}/100."
        )

        return SessionAnalysis(
            score=score,
            session=session,
            confidence=confidence,
            explanation=explanation,
        )


if __name__ == "__main__":

    provider = MarketDataProvider()

    market = provider.get_market_data("SPY")

    analyzer = SessionAnalyzer()

    result = analyzer.analyze(market)

    print("\n================================")
    print("STRATPILOT SESSION ANALYZER")
    print("================================")

    print(f"Symbol        : {market.symbol}")
    print(f"Timestamp     : {market.timestamp}")

    print(f"\nSession       : {result.session}")
    print(f"Score         : {result.score}/100")
    print(f"Confidence    : {result.confidence}")

    print("\nExplanation")
    print(result.explanation)

    print("\nThink First. Trade Second.")
