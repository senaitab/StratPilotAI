from dataclasses import dataclass

from intelligence.market_structure import build_demo_candles
from intelligence.swing_detector import SwingDetector


@dataclass(frozen=True)
class BOSResult:
    bullish: bool
    bearish: bool
    breakout_price: float
    broken_level: float
    confidence: int
    explanation: str


class BreakOfStructureAnalyzer:
    """
    Stage 31.2

    Determines whether price has broken the latest
    confirmed market structure.

    This module intentionally reuses the SwingDetector
    instead of implementing swing logic again.
    """

    def __init__(self) -> None:
        self.swing_detector = SwingDetector(window=1)

    def analyze(self, candles):

        swing_result = self.swing_detector.analyze(candles)

        latest_close = candles[-1].close

        latest_swing_high = swing_result.highs[-1].price
        latest_swing_low = swing_result.lows[-1].price

        bullish = latest_close > latest_swing_high
        bearish = latest_close < latest_swing_low

        if bullish:
            confidence = 95
            broken_level = latest_swing_high

            explanation = (
                "Price closed above the latest confirmed "
                "swing high. Bullish Break of Structure "
                "confirmed."
            )

        elif bearish:
            confidence = 95
            broken_level = latest_swing_low

            explanation = (
                "Price closed below the latest confirmed "
                "swing low. Bearish Break of Structure "
                "confirmed."
            )

        else:
            confidence = 45
            broken_level = latest_swing_high

            explanation = (
                "Price remains inside the current market "
                "structure. No confirmed Break of Structure."
            )

        return BOSResult(
            bullish=bullish,
            bearish=bearish,
            breakout_price=latest_close,
            broken_level=broken_level,
            confidence=confidence,
            explanation=explanation,
        )


if __name__ == "__main__":

    candles = build_demo_candles()

    analyzer = BreakOfStructureAnalyzer()

    result = analyzer.analyze(candles)

    print("\n====================================")
    print("STRATPILOT BREAK OF STRUCTURE")
    print("====================================")

    print(f"Current Close      : ${result.breakout_price:.2f}")
    print(f"Broken Level       : ${result.broken_level:.2f}")

    print(f"\nBullish BOS        : {result.bullish}")
    print(f"Bearish BOS        : {result.bearish}")

    print(f"\nConfidence         : {result.confidence}/100")

    print("\nExplanation")
    print(result.explanation)

    print("\nThink First. Trade Second.")
