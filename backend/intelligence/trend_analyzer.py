from dataclasses import dataclass
from typing import Optional

from intelligence.state import IntelligenceState


@dataclass
class TrendAnalysis:
    trend: str
    strength: int


class TrendAnalyzer:
    """
    Evaluates market trend and writes the result into the shared
    IntelligenceState object.

    Live price calculations will replace the placeholder values later.
    """

    def analyze(
        self,
        state: Optional[IntelligenceState] = None,
    ):
        trend = "TRENDING"
        strength = 92

        # Standalone mode preserves the original analyzer interface.
        if state is None:
            return TrendAnalysis(
                trend=trend,
                strength=strength,
            )

        # Shared-state pipeline mode.
        state.trend_score = strength
        return state


if __name__ == "__main__":
    analyzer = TrendAnalyzer()
    result = analyzer.analyze()

    print("\n==============================")
    print("STRATPILOT TREND ANALYZER")
    print("==============================")

    print(f"Trend    : {result.trend}")
    print(f"Strength : {result.strength}/100")

    print("\nThink First. Trade Second.")
