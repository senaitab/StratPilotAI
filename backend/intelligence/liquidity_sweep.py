from dataclasses import dataclass
from typing import Any, Sequence

from intelligence.market_structure import build_demo_candles
from intelligence.swing_detector import SwingDetector


@dataclass(frozen=True)
class LiquiditySweepResult:
    bullish_sweep: bool
    bearish_sweep: bool
    swept_level: float
    latest_swing_high: float
    latest_swing_low: float
    current_close: float
    confidence: int
    explanation: str


class LiquiditySweepAnalyzer:
    """
    Stage 31.4 — Liquidity Sweep Engine

    Detects:

    Bullish liquidity sweep:
    - Latest candle trades below the confirmed swing low.
    - Latest candle closes back above that swing low.

    Bearish liquidity sweep:
    - Latest candle trades above the confirmed swing high.
    - Latest candle closes back below that swing high.
    """

    def __init__(self, swing_window: int = 1) -> None:
        if swing_window < 1:
            raise ValueError("swing_window must be at least 1.")

        self.swing_detector = SwingDetector(window=swing_window)

    @staticmethod
    def _get_price(swing_point: Any) -> float:
        if hasattr(swing_point, "price"):
            return float(swing_point.price)

        if isinstance(swing_point, dict) and "price" in swing_point:
            return float(swing_point["price"])

        raise TypeError(
            "Swing point must contain a numeric 'price' value."
        )

    def analyze(
        self,
        candles: Sequence[Any],
    ) -> LiquiditySweepResult:
        if not candles:
            raise ValueError("At least one candle is required.")

        swing_result = self.swing_detector.analyze(candles)

        swing_highs = list(swing_result.highs)
        swing_lows = list(swing_result.lows)

        latest_candle = candles[-1]

        current_high = float(latest_candle.high)
        current_low = float(latest_candle.low)
        current_close = float(latest_candle.close)

        if not swing_highs or not swing_lows:
            return LiquiditySweepResult(
                bullish_sweep=False,
                bearish_sweep=False,
                swept_level=0.0,
                latest_swing_high=0.0,
                latest_swing_low=0.0,
                current_close=current_close,
                confidence=20,
                explanation=(
                    "Not enough confirmed swing data is available "
                    "to evaluate liquidity sweeps."
                ),
            )

        latest_swing_high = self._get_price(swing_highs[-1])
        latest_swing_low = self._get_price(swing_lows[-1])

        bullish_sweep = (
            current_low < latest_swing_low
            and current_close > latest_swing_low
        )

        bearish_sweep = (
            current_high > latest_swing_high
            and current_close < latest_swing_high
        )

        if bullish_sweep and bearish_sweep:
            swept_level = current_close
            confidence = 60
            explanation = (
                "The latest candle swept both the confirmed swing "
                "high and swing low before closing inside the range. "
                "This indicates elevated volatility and unclear "
                "directional liquidity intent."
            )

        elif bullish_sweep:
            swept_level = latest_swing_low
            confidence = 94
            explanation = (
                "Price traded below the latest confirmed swing low "
                "but closed back above it. Bullish liquidity sweep "
                "detected. Sellers may have been trapped."
            )

        elif bearish_sweep:
            swept_level = latest_swing_high
            confidence = 94
            explanation = (
                "Price traded above the latest confirmed swing high "
                "but closed back below it. Bearish liquidity sweep "
                "detected. Buyers may have been trapped."
            )

        else:
            swept_level = 0.0
            confidence = 45
            explanation = (
                "The latest candle did not reject beyond either "
                "confirmed swing level. No liquidity sweep is "
                "currently detected."
            )

        return LiquiditySweepResult(
            bullish_sweep=bullish_sweep,
            bearish_sweep=bearish_sweep,
            swept_level=swept_level,
            latest_swing_high=latest_swing_high,
            latest_swing_low=latest_swing_low,
            current_close=current_close,
            confidence=confidence,
            explanation=explanation,
        )


def main() -> None:
    candles = build_demo_candles()

    analyzer = LiquiditySweepAnalyzer(swing_window=1)
    result = analyzer.analyze(candles)

    print("\n====================================")
    print("STRATPILOT LIQUIDITY SWEEP")
    print("====================================")

    print(f"Latest Swing High : ${result.latest_swing_high:.2f}")
    print(f"Latest Swing Low  : ${result.latest_swing_low:.2f}")
    print(f"Current Close     : ${result.current_close:.2f}")

    print(f"\nBullish Sweep     : {result.bullish_sweep}")
    print(f"Bearish Sweep     : {result.bearish_sweep}")

    if result.swept_level > 0:
        print(f"Swept Level       : ${result.swept_level:.2f}")
    else:
        print("Swept Level       : None")

    print(f"\nConfidence        : {result.confidence}/100")

    print("\nExplanation")
    print(result.explanation)

    print("\nThink First. Trade Second.")


if __name__ == "__main__":
    main()
