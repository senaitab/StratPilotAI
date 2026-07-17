from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Candle:
    timestamp: str
    open_price: float
    high: float
    low: float
    close: float
    volume: int


@dataclass(frozen=True)
class StructureResult:
    trend: str
    structure: str
    score: int
    latest_swing_high: float
    previous_swing_high: float
    latest_swing_low: float
    previous_swing_low: float
    break_of_structure: bool
    change_of_character: bool
    explanation: str


class MarketStructureAnalyzer:
    """
    Stage 31.0 — Market Structure Engine

    Detects basic price structure from candle history:

    - Higher High / Higher Low
    - Lower High / Lower Low
    - Bullish or bearish Break of Structure
    - Basic Change of Character

    This foundation uses confirmed local swing points.
    Later stages will consume broker-provided candle history.
    """

    def __init__(self, swing_window: int = 2) -> None:
        if swing_window < 1:
            raise ValueError("swing_window must be at least 1.")

        self.swing_window = swing_window

    def analyze(
        self,
        candles: Sequence[Candle],
    ) -> StructureResult:
        self._validate_candles(candles)

        swing_highs = self._find_swing_highs(candles)
        swing_lows = self._find_swing_lows(candles)

        if len(swing_highs) < 2 or len(swing_lows) < 2:
            raise ValueError(
                "Not enough confirmed swing points. "
                "Provide more candle history."
            )

        previous_high = swing_highs[-2][1]
        latest_high = swing_highs[-1][1]

        previous_low = swing_lows[-2][1]
        latest_low = swing_lows[-1][1]

        higher_high = latest_high > previous_high
        higher_low = latest_low > previous_low
        lower_high = latest_high < previous_high
        lower_low = latest_low < previous_low

        latest_close = candles[-1].close

        bullish_bos = latest_close > latest_high
        bearish_bos = latest_close < latest_low
        break_of_structure = bullish_bos or bearish_bos

        if higher_high and higher_low:
            trend = "BULLISH"
            structure = "HIGHER HIGH + HIGHER LOW"
            score = 90

        elif lower_high and lower_low:
            trend = "BEARISH"
            structure = "LOWER HIGH + LOWER LOW"
            score = 90

        elif higher_high and lower_low:
            trend = "VOLATILE"
            structure = "EXPANDING RANGE"
            score = 55

        elif lower_high and higher_low:
            trend = "NEUTRAL"
            structure = "COMPRESSION"
            score = 50

        else:
            trend = "MIXED"
            structure = "UNCONFIRMED"
            score = 40

        if bullish_bos:
            score = min(score + 10, 100)

        if bearish_bos:
            score = min(score + 10, 100)

        change_of_character = (
            trend == "BULLISH" and bearish_bos
        ) or (
            trend == "BEARISH" and bullish_bos
        )

        if change_of_character:
            score = max(score - 25, 0)

        explanation = self._build_explanation(
            trend=trend,
            structure=structure,
            previous_high=previous_high,
            latest_high=latest_high,
            previous_low=previous_low,
            latest_low=latest_low,
            bullish_bos=bullish_bos,
            bearish_bos=bearish_bos,
            change_of_character=change_of_character,
        )

        return StructureResult(
            trend=trend,
            structure=structure,
            score=score,
            latest_swing_high=latest_high,
            previous_swing_high=previous_high,
            latest_swing_low=latest_low,
            previous_swing_low=previous_low,
            break_of_structure=break_of_structure,
            change_of_character=change_of_character,
            explanation=explanation,
        )

    def _find_swing_highs(
        self,
        candles: Sequence[Candle],
    ) -> list[tuple[int, float]]:
        swings: list[tuple[int, float]] = []
        window = self.swing_window

        for index in range(window, len(candles) - window):
            current_high = candles[index].high

            left = candles[index - window:index]
            right = candles[index + 1:index + window + 1]

            if all(
                current_high > candle.high
                for candle in left
            ) and all(
                current_high >= candle.high
                for candle in right
            ):
                swings.append((index, current_high))

        return swings

    def _find_swing_lows(
        self,
        candles: Sequence[Candle],
    ) -> list[tuple[int, float]]:
        swings: list[tuple[int, float]] = []
        window = self.swing_window

        for index in range(window, len(candles) - window):
            current_low = candles[index].low

            left = candles[index - window:index]
            right = candles[index + 1:index + window + 1]

            if all(
                current_low < candle.low
                for candle in left
            ) and all(
                current_low <= candle.low
                for candle in right
            ):
                swings.append((index, current_low))

        return swings

    @staticmethod
    def _build_explanation(
        trend: str,
        structure: str,
        previous_high: float,
        latest_high: float,
        previous_low: float,
        latest_low: float,
        bullish_bos: bool,
        bearish_bos: bool,
        change_of_character: bool,
    ) -> str:
        details = [
            f"Trend is {trend}.",
            f"Structure is {structure}.",
            (
                f"Swing highs moved from "
                f"${previous_high:.2f} to ${latest_high:.2f}."
            ),
            (
                f"Swing lows moved from "
                f"${previous_low:.2f} to ${latest_low:.2f}."
            ),
        ]

        if bullish_bos:
            details.append("Bullish break of structure detected.")

        if bearish_bos:
            details.append("Bearish break of structure detected.")

        if not bullish_bos and not bearish_bos:
            details.append("No confirmed break of structure.")

        if change_of_character:
            details.append(
                "Possible change of character detected."
            )

        return " ".join(details)

    @staticmethod
    def _validate_candles(
        candles: Sequence[Candle],
    ) -> None:
        if len(candles) < 10:
            raise ValueError(
                "At least 10 candles are required."
            )

        for candle in candles:
            if candle.high < candle.low:
                raise ValueError(
                    "Candle high cannot be below candle low."
                )

            if not candle.low <= candle.open_price <= candle.high:
                raise ValueError(
                    "Candle open must be between low and high."
                )

            if not candle.low <= candle.close <= candle.high:
                raise ValueError(
                    "Candle close must be between low and high."
                )

            if candle.volume < 0:
                raise ValueError(
                    "Candle volume cannot be negative."
                )


def build_demo_candles() -> list[Candle]:
    """
    Temporary candle history for Stage 31.0 testing.

    This will be replaced by broker candle data later.
    """

    values = [
        ("09:30", 100.0, 101.0, 99.5, 100.6),
        ("09:31", 100.6, 101.4, 100.2, 101.0),
        ("09:32", 101.0, 102.2, 100.7, 101.8),
        ("09:33", 101.8, 102.5, 101.1, 101.4),
        ("09:34", 101.4, 101.8, 100.8, 101.0),
        ("09:35", 101.0, 102.0, 100.9, 101.7),
        ("09:36", 101.7, 103.0, 101.5, 102.7),
        ("09:37", 102.7, 103.4, 102.0, 102.2),
        ("09:38", 102.2, 102.6, 101.6, 101.9),
        ("09:39", 101.9, 103.0, 101.8, 102.8),
        ("09:40", 102.8, 104.2, 102.5, 103.9),
        ("09:41", 103.9, 104.5, 103.2, 103.4),
        ("09:42", 103.4, 103.8, 102.8, 103.0),
        ("09:43", 103.0, 104.1, 102.9, 103.8),
        ("09:44", 103.8, 105.0, 103.6, 104.8),
    ]

    return [
        Candle(
            timestamp=timestamp,
            open_price=open_price,
            high=high,
            low=low,
            close=close,
            volume=1_000_000 + index * 100_000,
        )
        for index, (
            timestamp,
            open_price,
            high,
            low,
            close,
        ) in enumerate(values)
    ]


if __name__ == "__main__":
    analyzer = MarketStructureAnalyzer(swing_window=1)
    result = analyzer.analyze(build_demo_candles())

    print("\n====================================")
    print("STRATPILOT MARKET STRUCTURE ENGINE")
    print("====================================")

    print(f"Trend                : {result.trend}")
    print(f"Structure            : {result.structure}")
    print(f"Structure Score      : {result.score}/100")
    print(
        f"Previous Swing High  : "
        f"${result.previous_swing_high:.2f}"
    )
    print(
        f"Latest Swing High    : "
        f"${result.latest_swing_high:.2f}"
    )
    print(
        f"Previous Swing Low   : "
        f"${result.previous_swing_low:.2f}"
    )
    print(
        f"Latest Swing Low     : "
        f"${result.latest_swing_low:.2f}"
    )
    print(
        f"Break of Structure   : "
        f"{result.break_of_structure}"
    )
    print(
        f"Change of Character  : "
        f"{result.change_of_character}"
    )

    print("\nExplanation")
    print(result.explanation)

    print("\nThink First. Trade Second.")
