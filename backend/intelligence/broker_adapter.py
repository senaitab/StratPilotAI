from dataclasses import dataclass


# ---------------------------------
# INPUT
# ---------------------------------

@dataclass(frozen=True)
class ExecutionPlan:
    underlying: str
    action: str
    contract: str
    contracts: int
    order_type: str
    time_in_force: str
    approved: bool


# ---------------------------------
# OUTPUT
# ---------------------------------

@dataclass(frozen=True)
class BrokerOrder:
    symbol: str
    side: str
    quantity: int
    order_type: str
    tif: str


@dataclass(frozen=True)
class BrokerResponse:
    accepted: bool
    status: str
    explanation: str


class BrokerAdapter:

    def build_order(self, plan: ExecutionPlan) -> BrokerOrder:

        return BrokerOrder(
            symbol=plan.contract,
            side=plan.action,
            quantity=plan.contracts,
            order_type=plan.order_type,
            tif=plan.time_in_force,
        )

    def submit(self, plan: ExecutionPlan) -> BrokerResponse:

        if not plan.approved:
            return BrokerResponse(
                accepted=False,
                status="BLOCKED",
                explanation="Execution plan was not approved.",
            )

        order = self.build_order(plan)

        return BrokerResponse(
            accepted=True,
            status="PAPER_ACCEPTED",
            explanation=(
                f"Paper order created successfully for "
                f"{order.quantity} contract(s) of "
                f"{order.symbol}."
            ),
        )


def main():

    adapter = BrokerAdapter()

    plan = ExecutionPlan(
        underlying="SPY",
        action="BUY_CALL",
        contract="SPY 650 CALL",
        contracts=2,
        order_type="LIMIT",
        time_in_force="DAY",
        approved=True,
    )

    result = adapter.submit(plan)

    print("\n====================================")
    print("STRATPILOT BROKER ADAPTER")
    print("====================================")

    print(f"\nAccepted          : {result.accepted}")
    print(f"Status            : {result.status}")

    print("\nExplanation")
    print(result.explanation)

    print("\nThink First. Trade Second.")


if __name__ == "__main__":
    main()
