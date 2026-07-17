from dataclasses import dataclass
from typing import Sequence

from intelligence.market_structure import Candle, build_demo_candles


@dataclass(frozen=True)
class SwingPoint:
    index: int
    timestamp: str
    price: float
    kind: str


@dataclass(frozen=True)
class SwingAnalysis:
    highs: list[SwingPoint]
    lows: list[SwingPoint]
    higher_high: bool
    higher_low: bool
    lower_high: bool
    lower_low: bool
    structure: str
    explanation: str


class SwingDetector:
    """
    Stage 31.1 — Automatic Swing Detection

    Detects confirmed swing highs and swing lows from candle history.

    A swing is confirmed only after enough candles form on both sides,
    preventing the detector from treating the newest unfinished movement
    as a confirmed pivot.
    """

    def __init__(self, window: int = 1) -> None:
        if window < 1:
            raise ValueError("window must be at least 1.")

        self.window = window

    def analyze(
        self,
        candles: Sequence[Candle],
    ) -> SwingAnalysis:
        self._validate_candles(candles)

        highs = self.detect_highs(candles)
        lows = self.detect_lows(candles)

        if len(highs) < 2 or len(lows) < 2:
            raise ValueError(
                "At least two confirmed swing highs and two "
                "confirmed swing lows are required."
            )

        previous_high = highs[-2]
        latest_high = highs[-1]

        previous_low = lows[-2]
        latest_low = lows[-1]

        higher_high = latest_high.price > previous_high.price
        lower_high = latest_high.price < previous_high.price

        higher_low = latest_low.price > previous_low.price
        lower_low = latest_low.price < previous_low.price

        if higher_high and higher_low:
            structure = "BULLISH"

        elif lower_high and lower_low:
            structure = "BEARISH"

        elif lower_high and higher_low:
            structure = "COMPRESSION"

        elif higher_high and lower_low:
            structure = "EXPANDING RANGE"

        else:
            structure = "MIXED"

        explanation = self._build_explanation(
            previous_high=previous_high,
            latest_high=latest_high,
            previous_low=previous_low,
            latest_low=latest_low,
            structure=structure,
        )

        return SwingAnalysis(
            highs=highs,
            lows=lows,
            higher_high=higher_high,
            higher_low=higher_low,
            lower_high=lower_high,
            lower_low=lower_low,
            structure=structure,
            explanation=explanation,
        )

    def detect_highs(
        self,
        candles: Sequence[Candle],
    ) -> list[SwingPoint]:
        swings: list[SwingPoint] = []
        window = self.window

        for index in range(window, len(candles) - window):
            current = candles[index]

            left = candles[index - window:index]
            right = candles[index + 1:index + window + 1]

            is_swing_high = (
                all(current.high > candle.high for candle in left)
                and all(
                    current.high >= candle.high
                    for candle in right
                )
            )

            if is_swing_high:
                swings.append(
                    SwingPoint(
                        index=index,
                        timestamp=current.timestamp,
                        price=current.high,
                        kind="HIGH",
                    )
                )

        return swings

    def detect_lows(
        self,
        candles: Sequence[Candle],
    ) -> list[SwingPoint]:
        swings: list[SwingPoint] = []
        window = self.window

        for index in range(window, len(candles) - window):
            current = candles[index]

            left = candles[index - window:index]
            right = candles[index + 1:index + window + 1]

            is_swing_low = (
                all(current.low < candle.low for candle in left)
                and all(
                    current.low <= candle.low
                    for candle in right
                )
            )

            if is_swing_low:
                swings.append(
                    SwingPoint(
                        index=index,
                        timestamp=current.timestamp,
                        price=current.low,
                        kind="LOW",
                    )
                )

        return swings

    @staticmethod
    def _build_explanation(
        previous_high: SwingPoint,
        latest_high: SwingPoint,
        previous_low: SwingPoint,
        latest_low: SwingPoint,
        structure: str,
    ) -> str:
        return (
            f"Structure is {structure}. "
            f"Swing highs moved from "
            f"${previous_high.price:.2f} "
            f"to ${latest_high.price:.2f}. "
            f"Swing lows moved from "
            f"${previous_low.price:.2f} "
            f"to ${latest_low.price:.2f}."
        )

    def _validate_candles(
        self,
        candles: Sequence[Candle],
    ) -> None:
        minimum = self.window * 2 + 5

        if len(candles) < minimum:
            raise ValueError(
                f"At least {minimum} candles are required "
                f"for window={self.window}."
            )

        for index, candle in enumerate(candles):
            if candle.high < candle.low:
                raise ValueError(
                    f"Candle {index} high cannot be below low."
                )

            if not candle.low <= candle.open_price <= candle.high:
                raise ValueError(
                    f"Candle {index} open must be between low and high."
                )

            if not candle.low <= candle.close <= candle.high:
                raise ValueError(
                    f"Candle {index} close must be between low and high."
                )

            if candle.volume < 0:
                raise ValueError(
                    f"Candle {index} volume cannot be negative."
                )


def print_swings(
    title: str,
    swings: list[SwingPoint],
) -> None:
    print(f"\n{title}")
    print("-" * len(title))

    for swing in swings:
        print(
            f"Index {swing.index:>2} | "
            f"{swing.timestamp} | "
            f"${swing.price:.2f}"
        )


if __name__ == "__main__":
    candles = build_demo_candles()

    detector = SwingDetector(window=1)
    result = detector.analyze(candles)

    print("\n================================")
    print("STRATPILOT SWING DETECTOR")
    print("================================")

    print_swings("Detected Swing Highs", result.highs)
    print_swings("Detected Swing Lows", result.lows)

    print("\nCurrent Structure")
    print("-----------------")
    print(f"Higher High      : {result.higher_high}")
    print(f"Higher Low       : {result.higher_low}")
    print(f"Lower High       : {result.lower_high}")
    print(f"Lower Low        : {result.lower_low}")
    print(f"Structure        : {result.structure}")

    print("\nExplanation")
    print(result.explanation)

    print("\nThink First. Trade Second.")
