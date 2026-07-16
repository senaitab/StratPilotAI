from dataclasses import dataclass
from typing import Optional

from intelligence.state import IntelligenceState


@dataclass
class LiquidityAnalysis:
    level: str
    volume_score: int
    spread_score: int
    overall: str


class LiquidityAnalyzer:
    """
    Evaluates market liquidity and writes the resulting score into the
    shared IntelligenceState object.

    Volume and spread placeholders will be replaced with live data later.
    """

    def analyze(
        self,
        state: Optional[IntelligenceState] = None,
    ):
        volume_score = 94
        spread_score = 91

        average_score = round((volume_score + spread_score) / 2)

        if average_score >= 86:
            level = "EXCELLENT"
            overall = "TRADE"
        elif average_score >= 61:
            level = "GOOD"
            overall = "FAVORABLE"
        elif average_score >= 26:
            level = "FAIR"
            overall = "CAUTION"
        else:
            level = "POOR"
            overall = "AVOID"

        # Standalone mode.
        if state is None:
            return LiquidityAnalysis(
                level=level,
                volume_score=volume_score,
                spread_score=spread_score,
                overall=overall,
            )

        # Shared-state pipeline mode.
        state.liquidity_score = average_score
        return state


if __name__ == "__main__":
    analyzer = LiquidityAnalyzer()
    result = analyzer.analyze()

    print("\n==============================")
    print("STRATPILOT LIQUIDITY ANALYZER")
    print("==============================")

    print(f"Liquidity : {result.level}")
    print(f"Volume    : {result.volume_score}/100")
    print(f"Spread    : {result.spread_score}/100")
    print(f"\nOverall   : {result.overall}")

    print("\nThink First. Trade Second.")
