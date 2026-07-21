from dataclasses import dataclass
from time import perf_counter
from typing import Optional

from intelligence.decision_engine import (
    DecisionEngine,
    DemoConfluenceResult,
)
from intelligence.position_sizer import PositionSizer
from intelligence.risk_manager import RiskManager
from intelligence.trade_context import TradeContext


@dataclass(frozen=True)
class IntegrationResult:
    context: TradeContext
    runtime_seconds: float
    failed_module: Optional[str] = None


class TradeManager:
    """
    Stage 33.9

    Real integration of:
    1. Decision Engine
    2. Risk Manager
    3. Position Sizer
    4. Shared TradeContext
    """

    def __init__(self) -> None:
        self.decision_engine = DecisionEngine()
        self.risk_manager = RiskManager()
        self.position_sizer = PositionSizer()

    def run(
        self,
        confluence: DemoConfluenceResult,
        symbol: str = "SPY",
        account_balance: float = 10000.0,
        base_risk_percent: float = 1.0,
        risk_per_contract: float = 25.0,
    ) -> IntegrationResult:

        started_at = perf_counter()

        context = TradeContext(
            symbol=symbol,
            account_balance=account_balance,
            base_risk_percent=base_risk_percent,
            risk_per_contract=risk_per_contract,
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

        if not risk.trade_allowed:
            context.trade_status = "BLOCKED"

            return IntegrationResult(
                context=context,
                runtime_seconds=perf_counter() - started_at,
                failed_module="Risk Manager",
            )

        # ==========================================
        # 3. POSITION SIZER
        # ==========================================

        try:
            position = self.position_sizer.analyze(
                account_balance=context.account_balance,
                base_risk_percent=context.base_risk_percent,
                risk_result=risk,
                risk_per_contract=context.risk_per_contract,
            )

            context.account_balance = position.account_balance
            context.base_risk_percent = position.base_risk_percent
            context.effective_risk_percent = (
                position.effective_risk_percent
            )
            context.risk_amount = position.risk_amount
            context.risk_per_contract = position.risk_per_contract
            context.contracts = position.contracts
            context.position_explanation = position.explanation

            context.mark_complete("Position Sizer")

        except Exception as exc:
            context.add_error(
                f"Position Sizer failed: {exc}"
            )

            return IntegrationResult(
                context=context,
                runtime_seconds=perf_counter() - started_at,
                failed_module="Position Sizer",
            )

        # Position-sizing safety gate
        if context.contracts <= 0:
            context.add_error(
                "Position Sizer returned zero or fewer contracts."
            )

            return IntegrationResult(
                context=context,
                runtime_seconds=perf_counter() - started_at,
                failed_module="Position Sizer",
            )

        context.trade_status = "READY_FOR_CONTRACT_SELECTION"

        return IntegrationResult(
            context=context,
            runtime_seconds=perf_counter() - started_at,
        )


def print_summary(result: IntegrationResult) -> None:
    context = result.context

    print("\n====================================")
    print("STRATPILOT TRADE MANAGER")
    print("STAGE 33.9 - POSITION SIZER")
    print("====================================")

    print("\nDECISION ENGINE")

    print(f"Action             : {context.direction}")
    print(f"Setup Grade        : {context.setup_grade}")
    print(f"Confidence         : {context.confidence}/100")
    print(
        f"Decision Risk      : "
        f"{context.decision_risk_level}"
    )

    print("\nRISK MANAGER")

    print(
        f"Risk Level         : "
        f"{context.risk_level or 'NOT RUN'}"
    )
    print(
        f"Risk Multiplier    : "
        f"{context.risk_multiplier:.2f}x"
    )
    print(
        f"Trade Allowed      : "
        f"{context.trade_allowed}"
    )

    print("\nPOSITION SIZER")

    print(
        f"Account Balance    : "
        f"${context.account_balance:,.2f}"
    )
    print(
        f"Base Risk          : "
        f"{context.base_risk_percent:.2f}%"
    )
    print(
        f"Effective Risk     : "
        f"{context.effective_risk_percent:.2f}%"
    )
    print(
        f"Risk Amount        : "
        f"${context.risk_amount:,.2f}"
    )
    print(
        f"Risk Per Contract  : "
        f"${context.risk_per_contract:,.2f}"
    )
    print(
        f"Contracts          : "
        f"{context.contracts}"
    )

    print("\nPIPELINE")

    completed = (
        ", ".join(context.completed_modules)
        if context.completed_modules
        else "NONE"
    )

    print(f"Completed          : {completed}")
    print(f"Trade Status       : {context.trade_status}")
    print(
        f"Runtime            : "
        f"{result.runtime_seconds:.6f} sec"
    )

    if result.failed_module:
        print(
            f"Stopped At         : "
            f"{result.failed_module}"
        )

    if context.errors:
        print("\nERRORS")

        for error in context.errors:
            print(f"- {error}")

    print("\nEXPLANATION")

    if context.position_explanation:
        print(context.position_explanation)
    elif context.risk_explanation:
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
        base_risk_percent=1.0,
        risk_per_contract=25.0,
    )

    print_summary(result)


if __name__ == "__main__":
    main()
