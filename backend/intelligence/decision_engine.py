from dataclasses import dataclass
from typing import Literal


DecisionAction = Literal[
    "BUY_CALL",
    "BUY_PUT",
    "WAIT",
    "NO_TRADE",
]


@dataclass(frozen=True)
class DecisionResult:
    action: DecisionAction
    confidence: int
    setup_grade: str
    risk_level: str
    explanation: str


@dataclass(frozen=True)
class DemoConfluenceResult:
    trade_bias: str
    setup_grade: str
    confidence: int


class DecisionEngine:
    """
    Stage 32.0

    Converts market confluence into a trading decision.

    This engine DOES NOT execute trades.

    It only determines what StratPilot recommends.
    """

    BUY_CONFIDENCE = 70

    def analyze(
        self,
        confluence: DemoConfluenceResult,
    ) -> DecisionResult:

        bias = confluence.trade_bias.upper()

        grade = confluence.setup_grade.upper()

        confidence = confluence.confidence

        # ----------------------------
        # BUY CALL
        # ----------------------------

        if (
            bias == "BULLISH"
            and grade in ("A", "A+")
            and confidence >= self.BUY_CONFIDENCE
        ):

            return DecisionResult(
                action="BUY_CALL",
                confidence=confidence,
                setup_grade=grade,
                risk_level="LOW",
                explanation=(
                    "Bullish confluence satisfied all "
                    "Decision Engine requirements."
                ),
            )

        # ----------------------------
        # BUY PUT
        # ----------------------------

        if (
            bias == "BEARISH"
            and grade in ("A", "A+")
            and confidence >= self.BUY_CONFIDENCE
        ):

            return DecisionResult(
                action="BUY_PUT",
                confidence=confidence,
                setup_grade=grade,
                risk_level="LOW",
                explanation=(
                    "Bearish confluence satisfied all "
                    "Decision Engine requirements."
                ),
            )

        # ----------------------------
        # WAIT
        # ----------------------------

        if (
            bias != "NEUTRAL"
            and confidence >= 50
        ):

            return DecisionResult(
                action="WAIT",
                confidence=confidence,
                setup_grade=grade,
                risk_level="MEDIUM",
                explanation=(
                    "Directional bias exists, but the "
                    "overall evidence is not yet strong "
                    "enough to justify entering a trade."
                ),
            )

        # ----------------------------
        # NO TRADE
        # ----------------------------

        return DecisionResult(
            action="NO_TRADE",
            confidence=confidence,
            setup_grade=grade,
            risk_level="HIGH",
            explanation=(
                "Insufficient confluence. "
                "The best decision is patience."
            ),
        )


def main():

    confluence = DemoConfluenceResult(
        trade_bias="BULLISH",
        setup_grade="A+",
        confidence=80,
    )

    engine = DecisionEngine()

    result = engine.analyze(confluence)

    print("\n====================================")
    print("STRATPILOT DECISION ENGINE")
    print("====================================")

    print(f" Decision     : {result.action}")

    print(f" Risk Level   : {result.risk_level}")

    print(f" Confidence   : {result.confidence}/100")

    print(f" Setup Grade  : {result.setup_grade}")

    print("\n Explanation")

    print(f" {result.explanation}")

    print("\n Think First. Trade Second.")


if __name__ == "__main__":
    main()
