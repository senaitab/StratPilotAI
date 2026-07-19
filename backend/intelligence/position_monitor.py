from dataclasses import dataclass


@dataclass(frozen=True)
class PositionStatus:
    underlying: str
    contract: str
    contracts: int

    is_open: bool

    entry_price: float
    current_price: float

    unrealized_pl: float
    realized_pl: float
    return_percent: float

    stop_loss_active: bool
    take_profit_active: bool

    health: str
    exit_reason: str
    explanation: str


class PositionMonitor:
    """
    Stage 33.4 — Position Monitor

    Tracks an open options position and calculates:

    - Unrealized profit or loss
    - Percentage return
    - Position health
    - Stop-loss status
    - Take-profit status
    - Exit reason

    Option prices are multiplied by 100 because one standard
    option contract normally represents 100 shares.
    """

    OPTION_MULTIPLIER = 100

    def analyze(
        self,
        underlying: str,
        contract: str,
        contracts: int,
        entry_price: float,
        current_price: float,
        is_open: bool,
        realized_pl: float = 0.0,
    ) -> PositionStatus:
        if contracts < 0:
            raise ValueError(
                "Contracts cannot be negative."
            )

        if entry_price <= 0:
            raise ValueError(
                "Entry price must be greater than zero."
            )

        if current_price < 0:
            raise ValueError(
                "Current price cannot be negative."
            )

        price_change = current_price - entry_price

        unrealized_pl = (
            price_change
            * contracts
            * self.OPTION_MULTIPLIER
            if is_open
            else 0.0
        )

        return_percent = (
            price_change
            / entry_price
            * 100.0
        )

        if not is_open:
            health = "CLOSED"
            exit_reason = "POSITION CLOSED"
            stop_loss_active = False
            take_profit_active = False

            explanation = (
                "Position is closed. "
                "No additional monitoring is required."
            )

        elif current_price > entry_price:
            health = "STRONG"
            exit_reason = "NONE"
            stop_loss_active = True
            take_profit_active = True

            explanation = (
                "Position is profitable. "
                "No exit conditions have been triggered. "
                "Continue monitoring."
            )

        elif current_price == entry_price:
            health = "NEUTRAL"
            exit_reason = "NONE"
            stop_loss_active = True
            take_profit_active = True

            explanation = (
                "Position is currently at breakeven. "
                "Continue monitoring for directional movement."
            )

        else:
            health = "WEAK"
            exit_reason = "NONE"
            stop_loss_active = True
            take_profit_active = True

            explanation = (
                "Position is currently below the entry price. "
                "Monitor risk and exit conditions closely."
            )

        return PositionStatus(
            underlying=underlying,
            contract=contract,
            contracts=contracts,
            is_open=is_open,
            entry_price=entry_price,
            current_price=current_price,
            unrealized_pl=unrealized_pl,
            realized_pl=realized_pl,
            return_percent=return_percent,
            stop_loss_active=stop_loss_active,
            take_profit_active=take_profit_active,
            health=health,
            exit_reason=exit_reason,
            explanation=explanation,
        )


def main() -> None:
    monitor = PositionMonitor()

    result = monitor.analyze(
        underlying="SPY",
        contract="SPY 650 CALL",
        contracts=2,
        entry_price=3.25,
        current_price=3.92,
        is_open=True,
        realized_pl=0.0,
    )

    position_status = (
        "OPEN"
        if result.is_open
        else "CLOSED"
    )

    stop_status = (
        "ACTIVE"
        if result.stop_loss_active
        else "INACTIVE"
    )

    target_status = (
        "ACTIVE"
        if result.take_profit_active
        else "INACTIVE"
    )

    print("\n====================================")
    print("STRATPILOT POSITION MONITOR")
    print("====================================")

    print(f"\nUnderlying       : {result.underlying}")
    print(f"Contract         : {result.contract}")
    print(f"Status           : {position_status}")
    print(f"Contracts        : {result.contracts}")

    print(f"\nEntry Price      : ${result.entry_price:.2f}")
    print(f"Current Price    : ${result.current_price:.2f}")

    print(
        f"\nUnrealized P/L   : "
        f"{result.unrealized_pl:+.2f}"
    )

    print(
        f"Realized P/L     : "
        f"${result.realized_pl:.2f}"
    )

    print(
        f"Return           : "
        f"{result.return_percent:+.2f}%"
    )

    print(f"\nStop Loss        : {stop_status}")
    print(f"Take Profit      : {target_status}")

    print(f"\nPosition Health  : {result.health}")
    print(f"Exit Reason      : {result.exit_reason}")

    print("\nExplanation")
    print(result.explanation)

    print("\nThink First. Trade Second.")


if __name__ == "__main__":
    main()
