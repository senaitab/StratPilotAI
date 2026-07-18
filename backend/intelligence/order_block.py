from dataclasses import dataclass
from typing import Any, Optional, Sequence

from intelligence.market_structure import build_demo_candles


@dataclass(frozen=True)
class OrderBlockResult:
    bullish_block: bool
    bearish_block: bool
    block_high: float
    block_low: float
    breakout_level: float
    mitigated: bool
    confidence: int
    explanation: str


class OrderBlockAnalyzer:
    """
    Stage 31.6 — Order Block Engine

    Bullish Order Block:
        The final bearish candle before a bullish range breakout.

    Bearish Order Block:
        The final bullish candle before a bearish range breakout.

    The Candle model uses:
        candle.open_price
        candle.high
        candle.low
        candle.close
    """

    def __init__(self, lookback: int = 5) -> None:
        if lookback < 3:
            raise ValueError("Lookback must be at least 3.")

        self.lookback = lookback

    def analyze(
        self,
        candles: Sequence[Any],
    ) -> OrderBlockResult:
        required_candles = self.lookback + 1

        if len(candles) < required_candles:
            raise ValueError(
                f"At least {required_candles} candles are required "
                f"for a lookback of {self.lookback}."
            )

        breakout_candle = candles[-1]
        preceding_candles = candles[-required_candles:-1]

        previous_high = max(
            float(candle.high)
            for candle in preceding_candles
        )

        previous_low = min(
            float(candle.low)
            for candle in preceding_candles
        )

        latest_close = float(breakout_candle.close)

        bullish_breakout = latest_close > previous_high
        bearish_breakout = latest_close < previous_low

        if bullish_breakout:
            order_block = self._find_last_bearish_candle(
                preceding_candles
            )

            if order_block is None:
                return self._no_block_result(
                    explanation=(
                        "Bullish breakout detected, but no bearish "
                        "candle was found to define a bullish "
                        "Order Block."
                    ),
                    confidence=55,
                )

            block_high = float(order_block.high)
            block_low = float(order_block.low)

            return OrderBlockResult(
                bullish_block=True,
                bearish_block=False,
                block_high=block_high,
                block_low=block_low,
                breakout_level=previous_high,
                mitigated=False,
                confidence=92,
                explanation=(
                    "Bullish Order Block detected. The final bearish "
                    "candle before the bullish range breakout defines "
                    "the potential demand zone. The block has not yet "
                    "been evaluated against future candles for "
                    "mitigation."
                ),
            )

        if bearish_breakout:
            order_block = self._find_last_bullish_candle(
                preceding_candles
            )

            if order_block is None:
                return self._no_block_result(
                    explanation=(
                        "Bearish breakout detected, but no bullish "
                        "candle was found to define a bearish "
                        "Order Block."
                    ),
                    confidence=55,
                )

            block_high = float(order_block.high)
            block_low = float(order_block.low)

            return OrderBlockResult(
                bullish_block=False,
                bearish_block=True,
                block_high=block_high,
                block_low=block_low,
                breakout_level=previous_low,
                mitigated=False,
                confidence=92,
                explanation=(
                    "Bearish Order Block detected. The final bullish "
                    "candle before the bearish range breakout defines "
                    "the potential supply zone. The block has not yet "
                    "been evaluated against future candles for "
                    "mitigation."
                ),
            )

        return self._no_block_result(
            explanation=(
                "No qualifying range breakout occurred, so no new "
                "Order Block was confirmed."
            ),
            confidence=45,
        )

    @staticmethod
    def _find_last_bearish_candle(
        candles: Sequence[Any],
    ) -> Optional[Any]:
        for candle in reversed(candles):
            open_price = float(candle.open_price)
            close_price = float(candle.close)

            if close_price < open_price:
                return candle

        return None

    @staticmethod
    def _find_last_bullish_candle(
        candles: Sequence[Any],
    ) -> Optional[Any]:
        for candle in reversed(candles):
            open_price = float(candle.open_price)
            close_price = float(candle.close)

            if close_price > open_price:
                return candle

        return None

    @staticmethod
    def _no_block_result(
        explanation: str,
        confidence: int,
    ) -> OrderBlockResult:
        return OrderBlockResult(
            bullish_block=False,
            bearish_block=False,
            block_high=0.0,
            block_low=0.0,
            breakout_level=0.0,
            mitigated=False,
            confidence=confidence,
            explanation=explanation,
        )


def main() -> None:
    candles = build_demo_candles()

    if len(candles) < 4:
        raise ValueError(
            "The demo data must contain at least four candles."
        )

    lookback = min(5, len(candles) - 1)

    analyzer = OrderBlockAnalyzer(
        lookback=lookback
    )

    result = analyzer.analyze(candles)

    print("\n====================================")
    print("STRATPILOT ORDER BLOCK")
    print("====================================")

    print(f" Bullish Block : {result.bullish_block}")
    print(f" Bearish Block : {result.bearish_block}")

    if result.bullish_block or result.bearish_block:
        print(f"\n Block High    : ${result.block_high:.2f}")
        print(f" Block Low     : ${result.block_low:.2f}")
        print(
            f" Breakout Level: "
            f"${result.breakout_level:.2f}"
        )
    else:
        print("\n Block High    : None")
        print(" Block Low     : None")
        print(" Breakout Level: None")

    print(f"\n Mitigated     : {result.mitigated}")
    print(f"\n Confidence    : {result.confidence}/100")

    print("\n Explanation")
    print(f" {result.explanation}")

    print("\n Think First. Trade Second.")


if __name__ == "__main__":
    main()
