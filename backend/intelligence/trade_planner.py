from dataclasses import dataclass


# ==========================================
# INPUT MODELS
# ==========================================

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


# ==========================================
# FINAL TRADE PLAN
# ==========================================

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


# ==========================================
# TRADE PLANNER
# ==========================================

class TradePlanner:
    """
    Stage 34.1A

    Converts validated outputs from:

    1. Decision Engine
    2. Risk Manager
    3. Position Sizer
    4. Contract Selector

    into a complete execution-ready trade plan.
    """

    STOP_PERCENT = 0.15
    LIMIT_OFFSET = 0.01

    def analyze(
        self,
        decision: DecisionResult,
        risk: RiskResult,
        position: PositionSizeResult,
        contract: ContractSelectionResult,
    ) -> TradePlan:

        self._validate_inputs(
            decision=decision,
            risk=risk,
            position=position,
            contract=contract,
        )

        contract_name = self._build_contract_name(contract)

        entry_price = self._calculate_entry_price(contract)
        limit_price = self._calculate_limit_price(
            entry_price=entry_price,
            ask=contract.ask,
        )

        stop_loss = self._calculate_stop_loss(entry_price)

        risk_per_contract = round(
            entry_price - stop_loss,
            2,
        )

        target_1 = round(
            entry_price + risk_per_contract,
            2,
        )

        target_2 = round(
            entry_price + (risk_per_contract * 2),
            2,
        )

        target_3 = round(
            entry_price + (risk_per_contract * 3),
            2,
        )

        reward_per_contract = round(
            target_3 - entry_price,
            2,
        )

        risk_reward_ratio = self._calculate_risk_reward_ratio(
            risk_per_contract=risk_per_contract,
            reward_per_contract=reward_per_contract,
        )

        status = self._determine_status(
            decision=decision,
            position=position,
        )

        explanation = self._build_explanation(
            decision=decision,
            risk=risk,
            position=position,
            contract=contract,
            entry_price=entry_price,
            stop_loss=stop_loss,
            target_3=target_3,
            risk_reward_ratio=risk_reward_ratio,
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
            status=status,
            explanation=explanation,
        )

    # ==========================================
    # VALIDATION
    # ==========================================

    @staticmethod
    def _validate_inputs(
        decision: DecisionResult,
        risk: RiskResult,
        position: PositionSizeResult,
        contract: ContractSelectionResult,
    ) -> None:

        valid_actions = {
            "BUY_CALL",
            "BUY_PUT",
            "WAIT",
            "NO_TRADE",
        }

        if decision.action not in valid_actions:
            raise ValueError(
                f"Unsupported decision action: "
                f"{decision.action}"
            )

        if not 0 <= decision.confidence <= 100:
            raise ValueError(
                "Decision confidence must be "
                "between 0 and 100."
            )

        if not decision.setup_grade:
            raise ValueError(
                "Setup grade is required."
            )

        if risk.risk_multiplier < 0:
            raise ValueError(
                "Risk multiplier cannot be negative."
            )

        if position.contracts < 0:
            raise ValueError(
                "Contracts cannot be negative."
            )

        if position.risk_amount < 0:
            raise ValueError(
                "Risk amount cannot be negative."
            )

        if not contract.symbol:
            raise ValueError(
                "Contract symbol is required."
            )

        if contract.option_type not in {
            "CALL",
            "PUT",
        }:
            raise ValueError(
                "Option type must be CALL or PUT."
            )

        if contract.strike <= 0:
            raise ValueError(
                "Contract strike must be positive."
            )

        if not contract.expiration:
            raise ValueError(
                "Contract expiration is required."
            )

        if contract.bid <= 0:
            raise ValueError(
                "Contract bid must be positive."
            )

        if contract.ask <= 0:
            raise ValueError(
                "Contract ask must be positive."
            )

        if contract.ask < contract.bid:
            raise ValueError(
                "Contract ask cannot be lower "
                "than contract bid."
            )

    # ==========================================
    # PRICING
    # ==========================================

    @staticmethod
    def _calculate_entry_price(
        contract: ContractSelectionResult,
    ) -> float:

        midpoint = (
            contract.bid + contract.ask
        ) / 2

        return round(midpoint, 2)

    def _calculate_limit_price(
        self,
        entry_price: float,
        ask: float,
    ) -> float:

        suggested_limit = (
            entry_price + self.LIMIT_OFFSET
        )

        return round(
            min(ask, suggested_limit),
            2,
        )

    def _calculate_stop_loss(
        self,
        entry_price: float,
    ) -> float:

        stop_loss = entry_price * (
            1 - self.STOP_PERCENT
        )

        return round(
            max(stop_loss, 0.01),
            2,
        )

    # ==========================================
    # PLAN HELPERS
    # ==========================================

    @staticmethod
    def _build_contract_name(
        contract: ContractSelectionResult,
    ) -> str:

        strike = (
            str(int(contract.strike))
            if contract.strike.is_integer()
            else f"{contract.strike:g}"
        )

        return (
            f"{contract.symbol} "
            f"{strike} "
            f"{contract.option_type}"
        )

    @staticmethod
    def _calculate_risk_reward_ratio(
        risk_per_contract: float,
        reward_per_contract: float,
    ) -> float:

        if risk_per_contract <= 0:
            return 0.0

        return round(
            reward_per_contract
            / risk_per_contract,
            2,
        )

    @staticmethod
    def _determine_status(
        decision: DecisionResult,
        position: PositionSizeResult,
    ) -> str:

        if decision.action in {
            "WAIT",
            "NO_TRADE",
        }:
            return "NO_TRADE"

        if position.contracts <= 0:
            return "BLOCKED"

        return "READY_FOR_EXECUTION"

    @staticmethod
    def _build_explanation(
        decision: DecisionResult,
        risk: RiskResult,
        position: PositionSizeResult,
        contract: ContractSelectionResult,
        entry_price: float,
        stop_loss: float,
        target_3: float,
        risk_reward_ratio: float,
    ) -> str:

        return (
            "Trade plan assembled from Decision, "
            "Risk, Position Sizing and Contract "
            "Selection modules. "
            f"Action={decision.action}; "
            f"Confidence={decision.confidence}/100; "
            f"Setup={decision.setup_grade}; "
            f"Risk={risk.risk_level}; "
            f"Risk multiplier="
            f"{risk.risk_multiplier:.2f}x; "
            f"Contracts={position.contracts}; "
            f"Contract={contract.symbol} "
            f"{contract.strike:g} "
            f"{contract.option_type}; "
            f"Entry=${entry_price:.2f}; "
            f"Stop=${stop_loss:.2f}; "
            f"Final target=${target_3:.2f}; "
            f"Risk/Reward=1:{risk_reward_ratio:.2f}."
        )


# ==========================================
# DEMO
# ==========================================

def main() -> None:

    planner = TradePlanner()

    plan = planner.analyze(
        decision=DecisionResult(
            action="BUY_CALL",
            confidence=80,
            setup_grade="A+",
        ),
        risk=RiskResult(
            risk_level="MEDIUM",
            risk_multiplier=0.50,
        ),
        position=PositionSizeResult(
            contracts=2,
            risk_amount=50.0,
        ),
        contract=ContractSelectionResult(
            symbol="SPY",
            option_type="CALL",
            strike=649.0,
            expiration="2026-07-24",
            bid=3.00,
            ask=3.06,
        ),
    )

    print("\n====================================")
    print("STRATPILOT AI TRADE PLANNER")
    print("STAGE 34.1A FINAL")
    print("====================================")

    print(f"\nUnderlying        : {plan.underlying}")
    print(f"Action            : {plan.action}")
    print(f"Contract          : {plan.contract}")
    print(f"Expiration        : {plan.expiration}")

    print(f"\nContracts         : {plan.contracts}")
    print(f"Risk Level        : {plan.risk_level}")
    print(f"Risk Amount       : ${plan.risk_amount:.2f}")
    print(f"Confidence        : {plan.confidence}/100")
    print(f"Setup Grade       : {plan.setup_grade}")

    print("\nEXECUTION PRICES")
    print(f"Entry             : ${plan.entry_price:.2f}")
    print(f"Limit             : ${plan.limit_price:.2f}")
    print(f"Stop Loss         : ${plan.stop_loss:.2f}")

    print("\nPROFIT TARGETS")
    print(f"Target 1          : ${plan.target_1:.2f}")
    print(f"Target 2          : ${plan.target_2:.2f}")
    print(f"Target 3          : ${plan.target_3:.2f}")

    print("\nRISK / REWARD")
    print(
        f"Risk Per Contract : "
        f"${plan.risk_per_contract:.2f}"
    )
    print(
        f"Reward Per Contract: "
        f"${plan.reward_per_contract:.2f}"
    )
    print(
        f"Risk/Reward       : "
        f"1:{plan.risk_reward_ratio:.2f}"
    )

    print("\nSTATUS")
    print(plan.status)

    print("\nEXPLANATION")
    print(plan.explanation)

    print("\nThink First. Trade Second. 🤝🚀")


if __name__ == "__main__":
    main()
