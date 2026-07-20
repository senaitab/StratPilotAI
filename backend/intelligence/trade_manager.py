from dataclasses import dataclass
from time import perf_counter
from typing import Optional

from intelligence.decision_engine import (
    DecisionEngine,
    DemoConfluenceResult,
)
from intelligence.risk_manager import RiskManager
from intelligence.trade_context import TradeContext


@dataclass(frozen=True)
class IntegrationResult:
    context: TradeContext
    runtime_seconds: float
    failed_module: Optional[str] = None


class TradeManager:
    """
    Stage 33.8

    Real integration of:
    1. Decision Engine
    2. Risk Manager
    3. Shared TradeContext
    """

    def __init__(self) -> None:
        self.decision_engine = DecisionEngine()
        self.risk_manager = RiskManager()

    def run(
        self,
        confluence: DemoConfluenceResult,
        symbol: str = "SPY",
        account_balance: float = 10000.0,
    ) -> IntegrationResult:

        started_at = perf_counter()

        context = TradeContext(
            symbol=symbol,
            account_balance=account_balance,
            trade_status="ANALYZING",
        )

        # ==========================================
        # 1. DECISION ENGINE
        # ==========================================

        try:
            decision = self.decision_engine.analyze(confluence)

            context.direction = decision.action
            context.confidence = decision.confidence
            context.setup_grade = decision.setup_grade
            context.decision_risk_level = decision.risk_level
            context.decision_explanation = decision.explanation

            context.mark_complete("Decision Engine")

        except Exception as exc:
            context.add_error(
                f"Decision Engine failed: {exc}"
            )

            return IntegrationResult(
                context=context,
                runtime_seconds=perf_counter() - started_at,
                failed_module="Decision Engine",
            )

        # Stop if the Decision Engine does not approve an entry.
        if decision.action in {"WAIT", "NO_TRADE"}:
            context.trade_status = "NO_TRADE"

            return IntegrationResult(
                context=context,
                runtime_seconds=perf_counter() - started_at,
            )

        # ==========================================
        # 2. RISK MANAGER
        # ==========================================

        try:
            risk = self.risk_manager.analyze(decision)

            context.risk_level = risk.risk_level
            context.risk_multiplier = risk.risk_multiplier
            context.trade_allowed = risk.trade_allowed
            context.risk_explanation = risk.explanation

            context.mark_complete("Risk Manager")

        except Exception as exc:
            context.add_error(
                f"Risk Manager failed: {exc}"
            )

            return IntegrationResult(
                context=context,
                runtime_seconds=perf_counter() - started_at,
                failed_module="Risk Manager",
            )

        # Fail-fast risk gate.
        if not risk.trade_allowed:
            context.trade_status = "BLOCKED"

            return IntegrationResult(
                context=context,
                runtime_seconds=perf_counter() - started_at,
                failed_module="Risk Manager",
            )

        context.trade_status = "READY_FOR_SIZING"

        return IntegrationResult(
            context=context,
            runtime_seconds=perf_counter() - started_at,
        )


def print_summary(result: IntegrationResult) -> None:
    context = result.context

    print("\n====================================")
    print("STRATPILOT TRADE MANAGER")
    print("STAGE 33.8 - REAL INTEGRATION")
    print("====================================")

    print("\nDECISION ENGINE")

    print(f"Action          : {context.direction}")
    print(f"Setup Grade     : {context.setup_grade}")
    print(f"Confidence      : {context.confidence}/100")
    print(
        f"Decision Risk   : "
        f"{context.decision_risk_level}"
    )

    print("\nRISK MANAGER")

    print(
        f"Risk Level      : "
        f"{context.risk_level or 'NOT RUN'}"
    )

    print(
        f"Risk Multiplier : "
        f"{context.risk_multiplier:.2f}x"
    )

    print(
        f"Trade Allowed   : "
        f"{context.trade_allowed}"
    )

    print("\nPIPELINE")

    completed = (
        ", ".join(context.completed_modules)
        if context.completed_modules
        else "NONE"
    )

    print(f"Completed       : {completed}")
    print(f"Trade Status    : {context.trade_status}")
    print(f"Runtime         : {result.runtime_seconds:.6f} sec")

    if result.failed_module:
        print(f"Stopped At      : {result.failed_module}")

    if context.errors:
        print("\nERRORS")

        for error in context.errors:
            print(f"- {error}")

    print("\nEXPLANATION")

    if context.risk_explanation:
        print(context.risk_explanation)
    elif context.decision_explanation:
        print(context.decision_explanation)
    else:
        print("No explanation available.")

    print("\nThink First. Trade Second.")


def main() -> None:
    confluence = DemoConfluenceResult(
        trade_bias="BULLISH",
        setup_grade="A+",
        confidence=80,
    )

    manager = TradeManager()

    result = manager.run(
        confluence=confluence,
        symbol="SPY",
        account_balance=10000.0,
    )

    print_summary(result)


if __name__ == "__main__":
    main()
