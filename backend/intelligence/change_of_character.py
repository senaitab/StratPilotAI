from dataclasses import dataclass
from typing import Any, Sequence

from intelligence.market_structure import build_demo_candles
from intelligence.swing_detector import SwingDetector


@dataclass(frozen=True)
class CHoCHResult:
    bullish_change: bool
    bearish_change: bool
    previous_trend: str
    current_close: float
    reference_level: float
    confidence: int
    explanation: str


class ChangeOfCharacterAnalyzer:
    """
    Stage 31.3 — Change of Character Engine

    Detects an early potential market-structure reversal:

    - Bearish CHoCH:
      Previous structure was bullish and price closes below
      the latest confirmed swing low.

    - Bullish CHoCH:
      Previous structure was bearish and price closes above
      the latest confirmed swing high.
    """

    def __init__(self, swing_window: int = 1) -> None:
        if swing_window < 1:
            raise ValueError("swing_window must be at least 1.")

        self.swing_detector = SwingDetector(window=swing_window)

    @staticmethod
    def _get_price(swing_point: Any) -> float:
        """
        Safely extracts a price from the Swing Detector result.
        """

        if hasattr(swing_point, "price"):
            return float(swing_point.price)

        if isinstance(swing_point, dict) and "price" in swing_point:
            return float(swing_point["price"])

        raise TypeError(
            "Swing point must contain a numeric 'price' value."
        )

    def analyze(self, candles: Sequence[Any]) -> CHoCHResult:
        if not candles:
            raise ValueError("At least one candle is required.")

        swing_result = self.swing_detector.analyze(candles)

        swing_highs = list(swing_result.highs)
        swing_lows = list(swing_result.lows)

        if len(swing_highs) < 2 or len(swing_lows) < 2:
            return CHoCHResult(
                bullish_change=False,
                bearish_change=False,
                previous_trend="UNKNOWN",
                current_close=float(candles[-1].close),
                reference_level=0.0,
                confidence=20,
                explanation=(
                    "Not enough confirmed swing highs and swing lows "
                    "are available to determine Change of Character."
                ),
            )

        previous_high = self._get_price(swing_highs[-2])
        latest_high = self._get_price(swing_highs[-1])

        previous_low = self._get_price(swing_lows[-2])
        latest_low = self._get_price(swing_lows[-1])

        current_close = float(candles[-1].close)

        bullish_structure = (
            latest_high > previous_high
            and latest_low > previous_low
        )

        bearish_structure = (
            latest_high < previous_high
            and latest_low < previous_low
        )

        if bullish_structure:
            previous_trend = "BULLISH"
        elif bearish_structure:
            previous_trend = "BEARISH"
        else:
            previous_trend = "NEUTRAL"

        bearish_change = (
            previous_trend == "BULLISH"
            and current_close < latest_low
        )

        bullish_change = (
            previous_trend == "BEARISH"
            and current_close > latest_high
        )

        if bearish_change:
            reference_level = latest_low
            confidence = 92
            explanation = (
                "Previous market structure was bullish, but price "
                "closed below the latest confirmed swing low. "
                "Bearish Change of Character detected. This is an "
                "early warning of a possible bearish reversal."
            )

        elif bullish_change:
            reference_level = latest_high
            confidence = 92
            explanation = (
                "Previous market structure was bearish, but price "
                "closed above the latest confirmed swing high. "
                "Bullish Change of Character detected. This is an "
                "early warning of a possible bullish reversal."
            )

        else:
            if previous_trend == "BULLISH":
                reference_level = latest_low
            elif previous_trend == "BEARISH":
                reference_level = latest_high
            else:
                reference_level = current_close

            confidence = 45
            explanation = (
                "Price has not broken the opposing confirmed swing "
                "level. No Change of Character is currently detected."
            )

        return CHoCHResult(
            bullish_change=bullish_change,
            bearish_change=bearish_change,
            previous_trend=previous_trend,
            current_close=current_close,
            reference_level=reference_level,
            confidence=confidence,
            explanation=explanation,
        )


def main() -> None:
    candles = build_demo_candles()

    analyzer = ChangeOfCharacterAnalyzer(swing_window=1)
    result = analyzer.analyze(candles)

    print("\n====================================")
    print("STRATPILOT CHANGE OF CHARACTER")
    print("====================================")

    print(f"Previous Trend     : {result.previous_trend}")
    print(f"Current Close      : ${result.current_close:.2f}")
    print(f"Reference Level    : ${result.reference_level:.2f}")

    print(f"\nBullish CHoCH      : {result.bullish_change}")
    print(f"Bearish CHoCH      : {result.bearish_change}")

    print(f"\nConfidence         : {result.confidence}/100")

    print("\nExplanation")
    print(result.explanation)

    print("\nThink First. Trade Second.")


if __name__ == "__main__":
    main()
