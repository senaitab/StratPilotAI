from dataclasses import dataclass

from intelligence.market_data_provider import MarketData, MarketDataProvider


@dataclass
class LiquidityAnalysis:
    score: int
    status: str
    volume: int
    dollar_volume: float
    explanation: str


class LiquidityAnalyzer:
    """
    Stage 30.3

    Calculates a liquidity score from the shared MarketData object.

    This version uses:
    - Current trading volume
    - Estimated dollar volume

    Later stages can add:
    - Bid/ask spread
    - Average daily volume
    - Relative volume
    - Open interest
    - Order-book depth
    """

    def analyze(self, market: MarketData) -> LiquidityAnalysis:
        self._validate_market_data(market)

        dollar_volume = market.price * market.volume

        score = 20

        # Volume contribution
        if market.volume >= 150_000_000:
            score += 50
        elif market.volume >= 100_000_000:
            score += 40
        elif market.volume >= 50_000_000:
            score += 30
        elif market.volume >= 20_000_000:
            score += 20
        else:
            score += 10

        # Dollar-volume contribution
        if dollar_volume >= 100_000_000_000:
            score += 30
        elif dollar_volume >= 50_000_000_000:
            score += 25
        elif dollar_volume >= 20_000_000_000:
            score += 20
        elif dollar_volume >= 5_000_000_000:
            score += 15
        else:
            score += 5

        score = min(score, 100)

        if score >= 90:
            status = "EXCELLENT"
        elif score >= 75:
            status = "GOOD"
        elif score >= 50:
            status = "FAIR"
        else:
            status = "POOR"

        explanation = (
            f"Volume is {market.volume:,} shares with estimated "
            f"dollar volume of ${dollar_volume:,.2f}."
        )

        return LiquidityAnalysis(
            score=score,
            status=status,
            volume=market.volume,
            dollar_volume=dollar_volume,
            explanation=explanation,
        )

    @staticmethod
    def _validate_market_data(market: MarketData) -> None:
        if market.price <= 0:
            raise ValueError("Market price must be greater than zero.")

        if market.volume < 0:
            raise ValueError("Market volume cannot be negative.")


if __name__ == "__main__":
    provider = MarketDataProvider()
    market = provider.get_market_data("SPY")

    analyzer = LiquidityAnalyzer()
    result = analyzer.analyze(market)

    print("\n================================")
    print("STRATPILOT LIQUIDITY ANALYZER")
    print("================================")

    print(f"Symbol           : {market.symbol}")
    print(f"Price            : ${market.price:.2f}")
    print(f"Volume           : {result.volume:,}")
    print(f"Dollar Volume    : ${result.dollar_volume:,.2f}")

    print(f"\nLiquidity Score  : {result.score}/100")
    print(f"Status           : {result.status}")

    print("\nExplanation")
    print(result.explanation)

    print("\nThink First. Trade Second.")
