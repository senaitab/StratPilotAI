from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class ConfluenceResult:
    bullish_score: int
    bearish_score: int
    dominant_score: int
    trade_bias: str
    setup_grade: str
    confidence: int
    bullish_evidence: tuple[str, ...]
    bearish_evidence: tuple[str, ...]
    explanation: str


class ConfluenceEngine:
    """
    Stage 31.7 — Confluence Engine

    Combines structured evidence from:

    - Market Structure / Trend
    - Break of Structure
    - Change of Character
    - Liquidity Sweep
    - Fair Value Gap
    - Order Block

    Each analyzer remains independent. This engine only reads
    their completed result objects and scores the evidence.
    """

    WEIGHTS: Dict[str, int] = {
        "trend": 10,
        "bos": 20,
        "choch": 20,
        "liquidity_sweep": 15,
        "fair_value_gap": 15,
        "order_block": 20,
    }

    MAX_SCORE = sum(WEIGHTS.values())

    def analyze(
        self,
        structure_result: Any,
        bos_result: Any,
        choch_result: Any,
        liquidity_sweep_result: Any,
        fair_value_gap_result: Any,
        order_block_result: Any,
    ) -> ConfluenceResult:
        bullish_score = 0
        bearish_score = 0

        bullish_evidence: List[str] = []
        bearish_evidence: List[str] = []

        # ---------------------------------------------------------
        # Trend / Market Structure
        # ---------------------------------------------------------

        trend = str(
            getattr(structure_result, "trend", "")
        ).strip().upper()

        if trend == "BULLISH":
            bullish_score += self.WEIGHTS["trend"]
            bullish_evidence.append(
                f"Bullish market trend (+{self.WEIGHTS['trend']})"
            )

        elif trend == "BEARISH":
            bearish_score += self.WEIGHTS["trend"]
            bearish_evidence.append(
                f"Bearish market trend (+{self.WEIGHTS['trend']})"
            )

        # ---------------------------------------------------------
        # Break of Structure
        # ---------------------------------------------------------

        if bool(getattr(bos_result, "bullish", False)):
            bullish_score += self.WEIGHTS["bos"]
            bullish_evidence.append(
                f"Bullish Break of Structure "
                f"(+{self.WEIGHTS['bos']})"
            )

        if bool(getattr(bos_result, "bearish", False)):
            bearish_score += self.WEIGHTS["bos"]
            bearish_evidence.append(
                f"Bearish Break of Structure "
                f"(+{self.WEIGHTS['bos']})"
            )

        # ---------------------------------------------------------
        # Change of Character
        # ---------------------------------------------------------

        if bool(
            getattr(
                choch_result,
                "bullish_change",
                False,
            )
        ):
            bullish_score += self.WEIGHTS["choch"]
            bullish_evidence.append(
                f"Bullish Change of Character "
                f"(+{self.WEIGHTS['choch']})"
            )

        if bool(
            getattr(
                choch_result,
                "bearish_change",
                False,
            )
        ):
            bearish_score += self.WEIGHTS["choch"]
            bearish_evidence.append(
                f"Bearish Change of Character "
                f"(+{self.WEIGHTS['choch']})"
            )

        # ---------------------------------------------------------
        # Liquidity Sweep
        # ---------------------------------------------------------

        if bool(
            getattr(
                liquidity_sweep_result,
                "bullish_sweep",
                False,
            )
        ):
            bullish_score += self.WEIGHTS["liquidity_sweep"]
            bullish_evidence.append(
                f"Bullish liquidity sweep "
                f"(+{self.WEIGHTS['liquidity_sweep']})"
            )

        if bool(
            getattr(
                liquidity_sweep_result,
                "bearish_sweep",
                False,
            )
        ):
            bearish_score += self.WEIGHTS["liquidity_sweep"]
            bearish_evidence.append(
                f"Bearish liquidity sweep "
                f"(+{self.WEIGHTS['liquidity_sweep']})"
            )

        # ---------------------------------------------------------
        # Fair Value Gap
        # ---------------------------------------------------------

        if bool(
            getattr(
                fair_value_gap_result,
                "bullish_gap",
                False,
            )
        ):
            bullish_score += self.WEIGHTS["fair_value_gap"]
            bullish_evidence.append(
                f"Bullish Fair Value Gap "
                f"(+{self.WEIGHTS['fair_value_gap']})"
            )

        if bool(
            getattr(
                fair_value_gap_result,
                "bearish_gap",
                False,
            )
        ):
            bearish_score += self.WEIGHTS["fair_value_gap"]
            bearish_evidence.append(
                f"Bearish Fair Value Gap "
                f"(+{self.WEIGHTS['fair_value_gap']})"
            )

        # ---------------------------------------------------------
        # Order Block
        # ---------------------------------------------------------

        if bool(
            getattr(
                order_block_result,
                "bullish_block",
                False,
            )
        ):
            bullish_score += self.WEIGHTS["order_block"]
            bullish_evidence.append(
                f"Bullish Order Block "
                f"(+{self.WEIGHTS['order_block']})"
            )

        if bool(
            getattr(
                order_block_result,
                "bearish_block",
                False,
            )
        ):
            bearish_score += self.WEIGHTS["order_block"]
            bearish_evidence.append(
                f"Bearish Order Block "
                f"(+{self.WEIGHTS['order_block']})"
            )

        dominant_score = max(
            bullish_score,
            bearish_score,
        )

        trade_bias = self._determine_trade_bias(
            bullish_score=bullish_score,
            bearish_score=bearish_score,
        )

        setup_grade = self._determine_setup_grade(
            dominant_score=dominant_score,
            bullish_score=bullish_score,
            bearish_score=bearish_score,
        )

        confidence = self._calculate_confidence(
            dominant_score=dominant_score,
            bullish_score=bullish_score,
            bearish_score=bearish_score,
        )

        explanation = self._build_explanation(
            trade_bias=trade_bias,
            setup_grade=setup_grade,
            bullish_score=bullish_score,
            bearish_score=bearish_score,
        )

        return ConfluenceResult(
            bullish_score=bullish_score,
            bearish_score=bearish_score,
            dominant_score=dominant_score,
            trade_bias=trade_bias,
            setup_grade=setup_grade,
            confidence=confidence,
            bullish_evidence=tuple(bullish_evidence),
            bearish_evidence=tuple(bearish_evidence),
            explanation=explanation,
        )

    @staticmethod
    def _determine_trade_bias(
        bullish_score: int,
        bearish_score: int,
    ) -> str:
        score_difference = bullish_score - bearish_score

        if score_difference >= 20:
            return "BULLISH"

        if score_difference <= -20:
            return "BEARISH"

        return "NEUTRAL"

    @staticmethod
    def _determine_setup_grade(
        dominant_score: int,
        bullish_score: int,
        bearish_score: int,
    ) -> str:
        score_difference = abs(
            bullish_score - bearish_score
        )

        if score_difference < 20:
            return "NO TRADE"

        if dominant_score >= 80:
            return "A+"

        if dominant_score >= 60:
            return "A"

        if dominant_score >= 40:
            return "B"

        return "NO TRADE"

    def _calculate_confidence(
        self,
        dominant_score: int,
        bullish_score: int,
        bearish_score: int,
    ) -> int:
        if dominant_score == 0:
            return 0

        opposing_score = min(
            bullish_score,
            bearish_score,
        )

        conflict_penalty = opposing_score

        confidence = dominant_score - conflict_penalty

        return max(
            0,
            min(
                self.MAX_SCORE,
                confidence,
            ),
        )

    @staticmethod
    def _build_explanation(
        trade_bias: str,
        setup_grade: str,
        bullish_score: int,
        bearish_score: int,
    ) -> str:
        if trade_bias == "NEUTRAL":
            return (
                "Bullish and bearish evidence are too closely "
                "balanced. StratPilot should stand aside until "
                "a clearer directional advantage develops."
            )

        if setup_grade == "A+":
            strength = "Exceptional"

        elif setup_grade == "A":
            strength = "Strong"

        elif setup_grade == "B":
            strength = "Moderate"

        else:
            strength = "Insufficient"

        return (
            f"{strength} {trade_bias.lower()} confluence detected. "
            f"Bullish evidence scored {bullish_score}/100 and "
            f"bearish evidence scored {bearish_score}/100. "
            f"Setup grade: {setup_grade}."
        )


# -----------------------------------------------------------------
# Independent Stage 31.7 test objects
# -----------------------------------------------------------------

@dataclass(frozen=True)
class DemoStructureResult:
    trend: str


@dataclass(frozen=True)
class DemoBOSResult:
    bullish: bool
    bearish: bool


@dataclass(frozen=True)
class DemoCHoCHResult:
    bullish_change: bool
    bearish_change: bool


@dataclass(frozen=True)
class DemoLiquiditySweepResult:
    bullish_sweep: bool
    bearish_sweep: bool


@dataclass(frozen=True)
class DemoFairValueGapResult:
    bullish_gap: bool
    bearish_gap: bool


@dataclass(frozen=True)
class DemoOrderBlockResult:
    bullish_block: bool
    bearish_block: bool


def main() -> None:
    """
    Runs an independent deterministic test of the scoring engine.

    The real intelligence pipeline will later pass the actual
    analyzer results into ConfluenceEngine.analyze().
    """

    structure_result = DemoStructureResult(
        trend="BULLISH"
    )

    bos_result = DemoBOSResult(
        bullish=True,
        bearish=False,
    )

    choch_result = DemoCHoCHResult(
        bullish_change=False,
        bearish_change=False,
    )

    liquidity_sweep_result = DemoLiquiditySweepResult(
        bullish_sweep=True,
        bearish_sweep=False,
    )

    fair_value_gap_result = DemoFairValueGapResult(
        bullish_gap=True,
        bearish_gap=False,
    )

    order_block_result = DemoOrderBlockResult(
        bullish_block=True,
        bearish_block=False,
    )

    engine = ConfluenceEngine()

    result = engine.analyze(
        structure_result=structure_result,
        bos_result=bos_result,
        choch_result=choch_result,
        liquidity_sweep_result=liquidity_sweep_result,
        fair_value_gap_result=fair_value_gap_result,
        order_block_result=order_block_result,
    )

    print("\n====================================")
    print("STRATPILOT CONFLUENCE ENGINE")
    print("====================================")

    print(f" Bullish Score : {result.bullish_score}/100")
    print(f" Bearish Score : {result.bearish_score}/100")

    print(f"\n Trade Bias    : {result.trade_bias}")
    print(f" Setup Grade   : {result.setup_grade}")
    print(f" Confidence    : {result.confidence}/100")

    print("\n Bullish Evidence")

    if result.bullish_evidence:
        for evidence in result.bullish_evidence:
            print(f" + {evidence}")
    else:
        print(" None")

    print("\n Bearish Evidence")

    if result.bearish_evidence:
        for evidence in result.bearish_evidence:
            print(f" - {evidence}")
    else:
        print(" None")

    print("\n Explanation")
    print(f" {result.explanation}")

    print("\n Think First. Trade Second.")


if __name__ == "__main__":
    main()
