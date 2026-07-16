from dataclasses import dataclass

from intelligence.market_data_provider import MarketData, MarketDataProvider


@dataclass
class VolatilityAnalysis:
    score: int
    status: str
    intraday_range: float
    range_percent: float
    gap_percent: float
    explanation: str


class VolatilityAnalyzer:
    """
    Stage 30.2

    Calculates a volatility score from the shared MarketData object.

    This version uses:
    - Intraday high-to-low range
    - Intraday range as a percentage of price
    - Gap from previous close to current price

    Later stages can add ATR, VIX, historical volatility,
    implied volatility, and candle-based calculations.
    """

    def analyze(self, market: MarketData) -> VolatilityAnalysis:
        self._validate_market_data(market)

        intraday_range = market.high - market.low

        range_percent = (
            intraday_range / market.price
        ) * 100

        gap_percent = (
            abs(market.price - market.previous_close)
            / market.previous_close
        ) * 100

        score = 30

        # Intraday range contribution
        if range_percent >= 2.00:
            score += 45
        elif range_percent >= 1.25:
            score += 35
        elif range_percent >= 0.75:
            score += 25
        elif range_percent >= 0.35:
            score += 15
        else:
            score += 5

        # Gap contribution
        if gap_percent >= 1.50:
            score += 25
        elif gap_percent >= 1.00:
            score += 20
        elif gap_percent >= 0.50:
            score += 15
        elif gap_percent >= 0.20:
            score += 10
        else:
            score += 5

        score = min(score, 100)

        if score >= 90:
            status = "EXTREME"
        elif score >= 75:
            status = "HIGH"
        elif score >= 50:
            status = "NORMAL"
        else:
            status = "LOW"

        explanation = (
            f"Intraday range is ${intraday_range:.2f} "
            f"({range_percent:.2f}% of price). "
            f"Current price is {gap_percent:.2f}% away "
            f"from the previous close."
        )

        return VolatilityAnalysis(
            score=score,
            status=status,
            intraday_range=intraday_range,
            range_percent=range_percent,
            gap_percent=gap_percent,
            explanation=explanation,
        )

    @staticmethod
    def _validate_market_data(market: MarketData) -> None:
        if market.price <= 0:
            raise ValueError("Market price must be greater than zero.")

        if market.previous_close <= 0:
            raise ValueError(
                "Previous close must be greater than zero."
            )

        if market.high < market.low:
            raise ValueError(
                "Market high cannot be lower than market low."
            )

        if not (
            market.low <= market.price <= market.high
        ):
            raise ValueError(
                "Current price must be between the market low and high."
            )


if __name__ == "__main__":
    provider = MarketDataProvider()
    market = provider.get_market_data("SPY")

    analyzer = VolatilityAnalyzer()
    result = analyzer.analyze(market)

    print("\n================================")
    print("STRATPILOT VOLATILITY ANALYZER")
    print("================================")

    print(f"Symbol           : {market.symbol}")
    print(f"Price            : ${market.price:.2f}")
    print(f"High             : ${market.high:.2f}")
    print(f"Low              : ${market.low:.2f}")
    print(
        f"Previous Close   : "
        f"${market.previous_close:.2f}"
    )

    print(
        f"\nIntraday Range   : "
        f"${result.intraday_range:.2f}"
    )
    print(
        f"Range Percent    : "
        f"{result.range_percent:.2f}%"
    )
    print(
        f"Gap Percent      : "
        f"{result.gap_percent:.2f}%"
    )

    print(f"\nVolatility Score : {result.score}/100")
    print(f"Status           : {result.status}")

    print("\nExplanation")
    print(result.explanation)

    print("\nThink First. Trade Second.")
