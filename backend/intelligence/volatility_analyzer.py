from dataclasses import dataclass
from typing import Optional

from intelligence.state import IntelligenceState


@dataclass
class VolatilityAnalysis:
    level: str
    atr_score: int
    vix_score: int
    overall: str


class VolatilityAnalyzer:
    """
    Evaluates volatility and writes the resulting score into the shared
    IntelligenceState object.

    ATR and VIX placeholder values will be replaced by live data later.
    """

    def analyze(
        self,
        state: Optional[IntelligenceState] = None,
    ):
        atr_score = 81
        vix_score = 76

        average_score = round((atr_score + vix_score) / 2)

        if average_score >= 86:
            level = "EXTREME"
            overall = "AVOID"
        elif average_score >= 61:
            level = "HIGH"
            overall = "CAUTION"
        elif average_score >= 26:
            level = "NORMAL"
            overall = "GOOD"
        else:
            level = "LOW"
            overall = "QUIET"

        # Standalone mode.
        if state is None:
            return VolatilityAnalysis(
                level=level,
                atr_score=atr_score,
                vix_score=vix_score,
                overall=overall,
            )

        # Shared-state pipeline mode.
        state.volatility_score = average_score
        return state


if __name__ == "__main__":
    analyzer = VolatilityAnalyzer()
    result = analyzer.analyze()

    print("\n================================")
    print("STRATPILOT VOLATILITY ANALYZER")
    print("================================")

    print(f"Volatility : {result.level}")
    print(f"ATR Score  : {result.atr_score}/100")
    print(f"VIX Score  : {result.vix_score}/100")
    print(f"\nOverall    : {result.overall}")

    print("\nThink First. Trade Second.")
