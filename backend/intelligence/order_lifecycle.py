from dataclasses import dataclass
from enum import Enum


class OrderStatus(Enum):
    PENDING = "PENDING"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


@dataclass(frozen=True)
class Order:
    order_id: str
    symbol: str
    quantity: int
    filled_quantity: int
    status: OrderStatus


@dataclass(frozen=True)
class LifecycleResult:
    complete: bool
    explanation: str


class OrderLifecycleManager:

    def analyze(self, order: Order) -> LifecycleResult:

        if order.status == OrderStatus.FILLED:
            return LifecycleResult(
                complete=True,
                explanation="Order completely filled."
            )

        if order.status == OrderStatus.PARTIALLY_FILLED:
            remaining = order.quantity - order.filled_quantity
            return LifecycleResult(
                complete=False,
                explanation=(
                    f"Partial fill detected. "
                    f"{remaining} contract(s) remaining."
                ),
            )

        if order.status == OrderStatus.PENDING:
            return LifecycleResult(
                complete=False,
                explanation="Order is still pending."
            )

        if order.status == OrderStatus.CANCELLED:
            return LifecycleResult(
                complete=True,
                explanation="Order was cancelled."
            )

        if order.status == OrderStatus.REJECTED:
            return LifecycleResult(
                complete=True,
                explanation="Order was rejected."
            )

        return LifecycleResult(
            complete=True,
            explanation="Order expired."
        )


def main():

    manager = OrderLifecycleManager()

    order = Order(
        order_id="SPY001",
        symbol="SPY 650 CALL",
        quantity=2,
        filled_quantity=2,
        status=OrderStatus.FILLED,
    )

    result = manager.analyze(order)

    print("\n====================================")
    print("STRATPILOT ORDER LIFECYCLE")
    print("====================================")

    print(f"\nOrder Status      : {order.status.value}")
    print(f"Complete          : {result.complete}")

    print("\nExplanation")
    print(result.explanation)

    print("\nThink First. Trade Second.")


if __name__ == "__main__":
    main()
