from dataclasses import dataclass


# ----------------------------------------
# Input
# ----------------------------------------

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


# ----------------------------------------
# Output
# ----------------------------------------

@dataclass(frozen=True)
class ExecutionPlan:
    underlying: str
    action: str
    contract: str
    contracts: int
    order_type: str
    tif: str
    execution_status: str
    explanation: str


class ExecutionEngine:
    """
    Stage 33.0

    Converts an approved TradePlan
    into an ExecutionPlan.

    No broker communication yet.
    """

    def analyze(
        self,
        trade: TradePlan,
    ) -> ExecutionPlan:

        if trade.status != "READY TO EXECUTE":

            return ExecutionPlan(
                underlying=trade.underlying,
                action=trade.action,
                contract=trade.contract,
                contracts=trade.contracts,
                order_type="NONE",
                tif="DAY",
                execution_status="BLOCKED",
                explanation=(
                    "Trade plan is not approved "
                    "for execution."
                ),
            )

        return ExecutionPlan(
            underlying=trade.underlying,
            action=trade.action,
            contract=trade.contract,
            contracts=trade.contracts,
            order_type="LIMIT",
            tif="DAY",
            execution_status="WAITING FOR CONFIRMATION",
            explanation=(
                "Execution plan generated. "
                "Awaiting broker submission."
            ),
        )


def main():

    engine = ExecutionEngine()

    trade = TradePlan(
        underlying="SPY",
        action="BUY_CALL",
        contract="SPY 650 CALL",
        expiration="2026-07-24",
        contracts=2,
        confidence=80,
        setup_grade="A+",
        risk_level="MEDIUM",
        risk_amount=50.0,
        status="READY TO EXECUTE",
    )

    plan = engine.analyze(trade)

    print("\n====================================")
    print("STRATPILOT EXECUTION ENGINE")
    print("====================================")

    print(f"\nUnderlying        : {plan.underlying}")
    print(f"Action            : {plan.action}")
    print(f"Contract          : {plan.contract}")
    print(f"Contracts         : {plan.contracts}")

    print(f"\nOrder Type        : {plan.order_type}")
    print(f"Time In Force     : {plan.tif}")

    print(f"\nExecution Status")

    print(plan.execution_status)

    print("\nExplanation")

    print(plan.explanation)

    print("\nThink First. Trade Second.")


if __name__ == "__main__":
    main()
