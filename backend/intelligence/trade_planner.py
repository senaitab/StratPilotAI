from dataclasses import dataclass


# ============================================================
# Inputs from previous modules
# ============================================================

@dataclass(frozen=True)
class DecisionResult:
    action: str
    confidence: int
    setup_grade: str


@dataclass(frozen=True)
class RiskResult:
    risk_level: str
    risk_multiplier: float


@dataclass(frozen=True)
class PositionSizeResult:
    contracts: int
    risk_amount: float


@dataclass(frozen=True)
class ContractSelectionResult:
    symbol: str
    option_type: str
    strike: float
    expiration: str
    bid: float
    ask: float


# ============================================================
# Final Trade Plan
# ============================================================

@dataclass(frozen=True)
class TradePlan:
    underlying: str
    action: str
    contract: str
    expiration: str

    contracts: int
    confidence: int
    setup_grade: str

    risk_level: str
    risk_amount: float

    entry_price: float
    limit_price: float
    stop_loss: float

    target_1: float
    target_2: float
    target_3: float

    risk_per_contract: float
    reward_per_contract: float
    risk_reward_ratio: float

    status: str
    explanation: str


# ============================================================
# Trade Planner
# ============================================================

class TradePlanner:
    """
    Converts approved outputs from the Decision Engine,
    Risk Manager, Position Sizer, and Contract Selector
    into an execution-ready trade plan.

    This module does not place broker orders.
    """

    MIN_OPTION_PRICE = 0.01
    MIN_STOP_DISTANCE = 0.05

    def analyze(
        self,
        decision: DecisionResult,
        risk: RiskResult,
        position: PositionSizeResult,
        contract: ContractSelectionResult,
    ) -> TradePlan:

        self._validate_inputs(
            decision=decision,
            position=position,
            contract=contract,
        )

        contract_name = (
            f"{contract.symbol} "
            f"{self._format_strike(contract.strike)} "
            f"{contract.option_type.upper()}"
        )

        if decision.action == "NO_TRADE":
            return self._build_no_trade_plan(
                decision=decision,
                risk=risk,
                position=position,
                contract=contract,
                contract_name=contract_name,
            )

        # Midpoint represents the estimated fair option premium.
        midpoint = (contract.bid + contract.ask) / 2

        entry_price = self._round_price(midpoint)

        # Limit price is capped at the current ask.
        limit_price = self._round_price(
            min(contract.ask, midpoint + 0.01)
        )

        # Base stop uses a 15% premium decline.
        stop_distance = max(
            entry_price * 0.15,
            self.MIN_STOP_DISTANCE,
        )

        stop_loss = self._round_price(
            max(
                entry_price - stop_distance,
                self.MIN_OPTION_PRICE,
            )
        )

        actual_risk = entry_price - stop_loss

        # Profit targets use 1R, 2R, and 3R.
        target_1 = self._round_price(
            entry_price + actual_risk
        )
        target_2 = self._round_price(
            entry_price + actual_risk * 2
        )
        target_3 = self._round_price(
            entry_price + actual_risk * 3
        )

        risk_per_contract = self._round_money(
            actual_risk * 100
        )

        reward_per_contract = self._round_money(
            (target_3 - entry_price) * 100
        )

        risk_reward_ratio = (
            round(
                reward_per_contract / risk_per_contract,
                2,
            )
            if risk_per_contract > 0
            else 0.0
        )

        return TradePlan(
            underlying=contract.symbol,
            action=decision.action,
            contract=contract_name,
            expiration=contract.expiration,

            contracts=position.contracts,
            confidence=decision.confidence,
            setup_grade=decision.setup_grade,

            risk_level=risk.risk_level,
            risk_amount=position.risk_amount,

            entry_price=entry_price,
            limit_price=limit_price,
            stop_loss=stop_loss,

            target_1=target_1,
            target_2=target_2,
            target_3=target_3,

            risk_per_contract=risk_per_contract,
            reward_per_contract=reward_per_contract,
            risk_reward_ratio=risk_reward_ratio,

            status="READY_FOR_EXECUTION",

            explanation=(
                "Trade plan assembled from Decision, Risk, "
                "Position Sizing, and Contract Selection modules. "
                "Entry uses the option midpoint, the limit price is "
                "capped at the ask, and targets use 1R, 2R, and 3R."
            ),
        )

    def _validate_inputs(
        self,
        decision: DecisionResult,
        position: PositionSizeResult,
        contract: ContractSelectionResult,
    ) -> None:

        valid_actions = {
            "BUY_CALL",
            "BUY_PUT",
            "NO_TRADE",
        }

        if decision.action not in valid_actions:
            raise ValueError(
                f"Unsupported decision action: {decision.action}"
            )

        if not 0 <= decision.confidence <= 100:
            raise ValueError(
                "Decision confidence must be between 0 and 100."
            )

        if decision.action != "NO_TRADE":
            if position.contracts <= 0:
                raise ValueError(
                    "Position size must contain at least one contract."
                )

            if position.risk_amount <= 0:
                raise ValueError(
                    "Position risk amount must be greater than zero."
                )

        option_type = contract.option_type.upper()

        if option_type not in {"CALL", "PUT"}:
            raise ValueError(
                f"Unsupported option type: {contract.option_type}"
            )

        if contract.strike <= 0:
            raise ValueError(
                "Option strike must be greater than zero."
            )

        if contract.bid <= 0:
            raise ValueError(
                "Option bid must be greater than zero."
            )

        if contract.ask <= 0:
            raise ValueError(
                "Option ask must be greater than zero."
            )

        if contract.ask < contract.bid:
            raise ValueError(
                "Option ask cannot be lower than its bid."
            )

    def _build_no_trade_plan(
        self,
        decision: DecisionResult,
        risk: RiskResult,
        position: PositionSizeResult,
        contract: ContractSelectionResult,
        contract_name: str,
    ) -> TradePlan:

        return TradePlan(
            underlying=contract.symbol,
            action=decision.action,
            contract=contract_name,
            expiration=contract.expiration,

            contracts=0,
            confidence=decision.confidence,
            setup_grade=decision.setup_grade,

            risk_level=risk.risk_level,
            risk_amount=0.0,

            entry_price=0.0,
            limit_price=0.0,
            stop_loss=0.0,

            target_1=0.0,
            target_2=0.0,
            target_3=0.0,

            risk_per_contract=0.0,
            reward_per_contract=0.0,
            risk_reward_ratio=0.0,

            status="NO_TRADE",

            explanation=(
                "No trade plan was created because the "
                "Decision Engine returned NO_TRADE."
            ),
        )

    @staticmethod
    def _format_strike(strike: float) -> str:
        if strike.is_integer():
            return str(int(strike))

        return f"{strike:.2f}"

    @staticmethod
    def _round_price(value: float) -> float:
        return round(value + 1e-9, 2)

    @staticmethod
    def _round_money(value: float) -> float:
        return round(value + 1e-9, 2)


# ============================================================
# Standalone demonstration
# ============================================================

def main() -> None:

    planner = TradePlanner()

    plan = planner.analyze(
        DecisionResult(
            action="BUY_CALL",
            confidence=80,
            setup_grade="A+",
        ),
        RiskResult(
            risk_level="MEDIUM",
            risk_multiplier=0.50,
        ),
        PositionSizeResult(
            contracts=2,
            risk_amount=90.00,
        ),
        ContractSelectionResult(
            symbol="SPY",
            option_type="CALL",
            strike=649.0,
            expiration="2026-07-24",
            bid=3.00,
            ask=3.06,
        ),
    )

    print("\n==========================================")
    print("STRATPILOT AI TRADE PLANNER")
    print("STAGE 34.1")
    print("==========================================")

    print("\nTRADE")
    print(f"Underlying          : {plan.underlying}")
    print(f"Action              : {plan.action}")
    print(f"Contract            : {plan.contract}")
    print(f"Expiration          : {plan.expiration}")
    print(f"Contracts           : {plan.contracts}")

    print("\nSETUP")
    print(f"Confidence          : {plan.confidence}/100")
    print(f"Setup Grade         : {plan.setup_grade}")
    print(f"Risk Level          : {plan.risk_level}")
    print(f"Approved Risk       : ${plan.risk_amount:.2f}")

    print("\nEXECUTION PLAN")
    print(f"Entry Price         : ${plan.entry_price:.2f}")
    print(f"Limit Price         : ${plan.limit_price:.2f}")
    print(f"Stop Loss           : ${plan.stop_loss:.2f}")
    print(f"Target 1            : ${plan.target_1:.2f}")
    print(f"Target 2            : ${plan.target_2:.2f}")
    print(f"Target 3            : ${plan.target_3:.2f}")

    print("\nRISK / REWARD")
    print(
        f"Risk Per Contract   : "
        f"${plan.risk_per_contract:.2f}"
    )
    print(
        f"Reward Per Contract : "
        f"${plan.reward_per_contract:.2f}"
    )
    print(
        f"Risk Reward         : "
        f"1:{plan.risk_reward_ratio:.2f}"
    )

    print("\nSTATUS")
    print(plan.status)

    print("\nEXPLANATION")
    print(plan.explanation)

    print("\nThink First. Trade Second. 🤝🚀")


if __name__ == "__main__":
    main()
