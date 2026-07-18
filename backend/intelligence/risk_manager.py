from dataclasses import dataclass
from typing import Literal


RiskLevel = Literal[
    "LOW",
    "MEDIUM",
    "HIGH",
    "NO_RISK",
]


@dataclass(frozen=True)
class DecisionResult:
    action: str
    confidence: int
    setup_grade: str
    risk_level: str
    explanation: str


@dataclass(frozen=True)
class RiskResult:
    risk_level: RiskLevel
    risk_multiplier: float
    trade_allowed: bool
    explanation: str


class RiskManager:
    """
    Stage 32.1

    Converts a trading decision into a risk profile.

    This module DOES NOT calculate position size.

    It only determines how aggressively StratPilot
    should be willing to risk capital.
    """

    def analyze(
        self,
        decision: DecisionResult,
    ) -> RiskResult:

        action = decision.action.upper()
        confidence = decision.confidence

        # -----------------------
        # NO TRADE
        # -----------------------

        if action == "NO_TRADE":
            return RiskResult(
                risk_level="NO_RISK",
                risk_multiplier=0.0,
                trade_allowed=False,
                explanation=(
                    "No trade was approved. "
                    "Capital remains protected."
                ),
            )

        # -----------------------
        # WAIT
        # -----------------------

        if action == "WAIT":
            return RiskResult(
                risk_level="HIGH",
                risk_multiplier=0.25,
                trade_allowed=False,
                explanation=(
                    "Directional bias exists, "
                    "but patience is preferred."
                ),
            )

        # -----------------------
        # Strong setup
        # -----------------------

        if confidence >= 85:
            return RiskResult(
                risk_level="LOW",
                risk_multiplier=1.00,
                trade_allowed=True,
                explanation=(
                    "Exceptional setup. "
                    "Normal risk allocation approved."
                ),
            )

        # -----------------------
        # Good setup
        # -----------------------

        if confidence >= 70:
            return RiskResult(
                risk_level="MEDIUM",
                risk_multiplier=0.50,
                trade_allowed=True,
                explanation=(
                    "Good setup. "
                    "Reduced risk allocation recommended."
                ),
            )

        # -----------------------
        # Weak setup
        # -----------------------

        return RiskResult(
            risk_level="HIGH",
            risk_multiplier=0.25,
            trade_allowed=False,
            explanation=(
                "Confidence is below the minimum "
                "threshold. Preserve capital."
            ),
        )


def main():

    decision = DecisionResult(
        action="BUY_CALL",
        confidence=80,
        setup_grade="A+",
        risk_level="LOW",
        explanation="Bullish confluence.",
    )

    manager = RiskManager()

    result = manager.analyze(decision)

    print("\n====================================")
    print("STRATPILOT RISK MANAGER")
    print("====================================")

    print(f" Risk Level       : {result.risk_level}")

    print(
        f" Risk Multiplier  : "
        f"{result.risk_multiplier:.2f}x"
    )

    print(
        f" Trade Allowed    : "
        f"{result.trade_allowed}"
    )

    print("\n Explanation")

    print(f" {result.explanation}")

    print("\n Think First. Trade Second.")


if __name__ == "__main__":
    main()
