from dataclasses import dataclass


# ---------------------------------
# Inputs from previous modules
# ---------------------------------

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


# ---------------------------------
# Final Trade Plan
# ---------------------------------

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
    status: str
    explanation: str


class TradePlanner:

    def analyze(
        self,
        decision: DecisionResult,
        risk: RiskResult,
        position: PositionSizeResult,
        contract: ContractSelectionResult,
    ) -> TradePlan:

        contract_name = (
            f"{contract.symbol} "
            f"{int(contract.strike)} "
            f"{contract.option_type}"
        )

        status = (
            "READY TO EXECUTE"
            if decision.action != "NO_TRADE"
            else "NO TRADE"
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
            status=status,
            explanation=(
                "Trade plan assembled from Decision, "
                "Risk, Position Sizing and "
                "Contract Selection modules."
            ),
        )


def main():

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
            risk_amount=50.0,
        ),

        ContractSelectionResult(
            symbol="SPY",
            option_type="CALL",
            strike=650,
            expiration="2026-07-24",
        ),
    )

    print("\n====================================")
    print("STRATPILOT TRADE PLANNER")
    print("====================================")

    print(f"\nUnderlying      : {plan.underlying}")
    print(f"Action          : {plan.action}")
    print(f"Contract        : {plan.contract}")
    print(f"Expiration      : {plan.expiration}")

    print(f"\nContracts       : {plan.contracts}")

    print(f"Risk Level      : {plan.risk_level}")

    print(f"Risk Amount     : ${plan.risk_amount:.2f}")

    print(f"Confidence      : {plan.confidence}/100")

    print(f"Setup Grade     : {plan.setup_grade}")

    print(f"\nStatus")

    print(plan.status)

    print(f"\nExplanation")

    print(plan.explanation)

    print("\nThink First. Trade Second.")


if __name__ == "__main__":
    main()
