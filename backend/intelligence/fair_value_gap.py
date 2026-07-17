from dataclasses import dataclass
from typing import Sequence, Any

from intelligence.market_structure import build_demo_candles


@dataclass(frozen=True)
class FairValueGapResult:
    bullish_gap: bool
    bearish_gap: bool
    gap_top: float
    gap_bottom: float
    filled: bool
    confidence: int
    explanation: str


class FairValueGapAnalyzer:
    """
    Stage 31.5

    Detects Fair Value Gaps (FVG)
    using a simple three-candle model.

    Bullish FVG:
        Candle3.low > Candle1.high

    Bearish FVG:
        Candle3.high < Candle1.low
    """

    def analyze(
        self,
        candles: Sequence[Any],
    ) -> FairValueGapResult:

        if len(candles) < 3:
            raise ValueError(
                "At least three candles are required."
            )

        c1 = candles[-3]
        c2 = candles[-2]
        c3 = candles[-1]

        bullish_gap = c3.low > c1.high
        bearish_gap = c3.high < c1.low

        gap_top = 0.0
        gap_bottom = 0.0
        filled = False

        if bullish_gap:

            gap_bottom = float(c1.high)
            gap_top = float(c3.low)

            filled = (
                float(c3.low) <= gap_bottom
            )

            confidence = 92

            explanation = (
                "Bullish Fair Value Gap detected. "
                "Price moved aggressively higher, "
                "leaving an imbalance."
            )

        elif bearish_gap:

            gap_top = float(c1.low)
            gap_bottom = float(c3.high)

            filled = (
                float(c3.high) >= gap_top
            )

            confidence = 92

            explanation = (
                "Bearish Fair Value Gap detected. "
                "Price moved aggressively lower, "
                "leaving an imbalance."
            )

        else:

            confidence = 45

            explanation = (
                "No Fair Value Gap detected."
            )

        return FairValueGapResult(
            bullish_gap=bullish_gap,
            bearish_gap=bearish_gap,
            gap_top=gap_top,
            gap_bottom=gap_bottom,
            filled=filled,
            confidence=confidence,
            explanation=explanation,
        )


def main():

    candles = build_demo_candles()

    analyzer = FairValueGapAnalyzer()

    result = analyzer.analyze(candles)

    print("\n====================================")
    print("STRATPILOT FAIR VALUE GAP")
    print("====================================")

    print(f"Bullish Gap : {result.bullish_gap}")
    print(f"Bearish Gap : {result.bearish_gap}")

    if result.gap_top > 0:

        print(f"\nGap Top     : ${result.gap_top:.2f}")
        print(f"Gap Bottom  : ${result.gap_bottom:.2f}")

    else:

        print("\nGap Top     : None")
        print("Gap Bottom  : None")

    print(f"\nFilled      : {result.filled}")

    print(f"\nConfidence  : {result.confidence}/100")

    print("\nExplanation")
    print(result.explanation)

    print("\nThink First. Trade Second.")


if __name__ == "__main__":
    main()
