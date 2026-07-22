from dataclasses import dataclass
from time import perf_counter
from typing import Optional

from intelligence.contract_selector import (
    ContractSelector,
    OptionContract,
)
from intelligence.decision_engine import (
    DecisionEngine,
    DemoConfluenceResult,
)
from intelligence.position_sizer import PositionSizer
from intelligence.risk_manager import RiskManager
from intelligence.trade_context import TradeContext
from intelligence.trade_planner import (
    ContractSelectionResult as PlannerContractSelectionResult,
    DecisionResult as PlannerDecisionResult,
    PositionSizeResult as PlannerPositionSizeResult,
    RiskResult as PlannerRiskResult,
    TradePlanner,
)


@dataclass(frozen=True)
class IntegrationResult:
    context: TradeContext
    runtime_seconds: float
    failed_module: Optional[str] = None


class TradeManager:
    """
    Stage 34.0

    Real integration of:
    1. Decision Engine
    2. Risk Manager
    3. Position Sizer
    4. Contract Selector
    5. Shared TradeContext
    """

    def __init__(self) -> None:
        self.decision_engine = DecisionEngine()
        self.risk_manager = RiskManager()
        self.position_sizer = PositionSizer()
        self.contract_selector = ContractSelector()
        self.trade_planner = TradePlanner()

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

        if context.contracts <= 0:
            context.add_error(
                "Position Sizer returned zero or fewer contracts."
            )

            return IntegrationResult(
                context=context,
                runtime_seconds=perf_counter() - started_at,
                failed_module="Position Sizer",
            )

        # ==========================================
        # 4. CONTRACT SELECTOR
        # ==========================================

        try:
            option_type = (
                "CALL"
                if context.direction == "BUY_CALL"
                else "PUT"
            )

            contract_candidates = [
                OptionContract(
                    symbol=context.symbol,
                    option_type=option_type,
                    strike=648,
                    expiration="2026-07-24",
                    delta=0.35,
                    bid=2.10,
                    ask=2.25,
                    volume=450,
                    open_interest=1200,
                ),
                OptionContract(
                    symbol=context.symbol,
                    option_type=option_type,
                    strike=649,
                    expiration="2026-07-24",
                    delta=0.52,
                    bid=3.00,
                    ask=3.06,
                    volume=1800,
                    open_interest=4200,
                ),
                OptionContract(
                    symbol=context.symbol,
                    option_type=option_type,
                    strike=650,
                    expiration="2026-07-24",
                    delta=0.41,
                    bid=2.55,
                    ask=2.63,
                    volume=950,
                    open_interest=2600,
                ),
            ]

            selection = self.contract_selector.analyze(
                contract_candidates
            )

            selected = selection.contract

            if selected is None:
                raise ValueError(
                    "Contract Selector returned no contract."
                )

            context.selected_symbol = selected.symbol
            context.selected_option_type = selected.option_type
            context.selected_strike = selected.strike
            context.selected_expiration = selected.expiration
            context.selected_delta = selected.delta
            context.liquidity_score = selection.liquidity_score
            context.overall_score = selection.overall_score
            context.contract_explanation = selection.explanation

            context.mark_complete("Contract Selector")

        except Exception as exc:
            context.add_error(
                f"Contract Selector failed: {exc}"
            )

            return IntegrationResult(
                context=context,
                runtime_seconds=perf_counter() - started_at,
                failed_module="Contract Selector",
            )

        if not context.selected_symbol:
            context.add_error(
                "Contract Selector did not select a valid contract."
            )

            return IntegrationResult(
                context=context,
                runtime_seconds=perf_counter() - started_at,
                failed_module="Contract Selector",
            )

        # ==========================================
        # 5. TRADE PLANNER
        # ==========================================

        try:
            planner_decision = PlannerDecisionResult(
                action=context.direction,
                confidence=context.confidence,
                setup_grade=context.setup_grade,
            )

            planner_risk = PlannerRiskResult(
                risk_level=context.risk_level,
                risk_multiplier=context.risk_multiplier,
            )

            planner_position = PlannerPositionSizeResult(
                contracts=context.contracts,
                risk_amount=context.risk_amount,
            )

            planner_contract = PlannerContractSelectionResult(
                symbol=selected.symbol,
                option_type=selected.option_type,
                strike=float(selected.strike),
                expiration=selected.expiration,
                bid=selected.bid,
                ask=selected.ask,
            )

            plan = self.trade_planner.analyze(
                decision=planner_decision,
                risk=planner_risk,
                position=planner_position,
                contract=planner_contract,
            )

            context.trade_plan = plan
            context.trade_status = plan.status
            context.mark_complete("Trade Planner")

        except Exception as exc:
            context.add_error(
                f"Trade Planner failed: {exc}"
            )

            return IntegrationResult(
                context=context,
                runtime_seconds=perf_counter() - started_at,
                failed_module="Trade Planner",
            )

        if context.trade_plan is None:
            context.add_error(
                "Trade Planner did not create a valid trade plan."
            )

            return IntegrationResult(
                context=context,
                runtime_seconds=perf_counter() - started_at,
                failed_module="Trade Planner",
            )

        return IntegrationResult(
            context=context,
            runtime_seconds=perf_counter() - started_at,
        )


def print_summary(result: IntegrationResult) -> None:
    context = result.context
    plan = context.trade_plan

    print("\n====================================")
    print("STRATPILOT TRADE MANAGER")
    print("STAGE 34.1B - TRADE PLANNER")
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

    print("\nCONTRACT SELECTOR")

    if context.selected_symbol:
        selected_contract = (
            f"{context.selected_symbol} "
            f"{context.selected_strike:g} "
            f"{context.selected_option_type}"
        )
    else:
        selected_contract = "NOT SELECTED"

    print(
        f"Selected Contract  : "
        f"{selected_contract}"
    )
    print(
        f"Expiration         : "
        f"{context.selected_expiration or 'N/A'}"
    )
    print(
        f"Delta              : "
        f"{context.selected_delta:.2f}"
    )
    print(
        f"Liquidity Score    : "
        f"{context.liquidity_score}/100"
    )
    print(
        f"Overall Score      : "
        f"{context.overall_score}/100"
    )

    print("\nTRADE PLANNER")

    if plan is not None:
        print(f"Contract           : {plan.contract}")
        print(f"Expiration         : {plan.expiration}")
        print(f"Contracts          : {plan.contracts}")
        print(f"Entry              : ${plan.entry_price:.2f}")
        print(f"Limit              : ${plan.limit_price:.2f}")
        print(f"Stop Loss          : ${plan.stop_loss:.2f}")
        print(f"Target 1           : ${plan.target_1:.2f}")
        print(f"Target 2           : ${plan.target_2:.2f}")
        print(f"Target 3           : ${plan.target_3:.2f}")
        print(
            f"Risk/Reward        : "
            f"1:{plan.risk_reward_ratio:.2f}"
        )
        print(f"Plan Status        : {plan.status}")
    else:
        print("Trade Plan         : NOT CREATED")

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

    if plan is not None:
        print(plan.explanation)
    elif context.contract_explanation:
        print(context.contract_explanation)
    elif context.position_explanation:
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
