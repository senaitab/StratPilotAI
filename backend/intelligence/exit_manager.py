from dataclasses import dataclass


@dataclass(frozen=True)
class PositionStatus:
    health: str
    unrealized_pl: float
    return_percent: float
    stop_loss_active: bool
    take_profit_active: bool


@dataclass(frozen=True)
class ExitDecision:
    should_exit: bool
    exit_type: str
    confidence: int
    explanation: str


class ExitManager:
    """
    Stage 33.5

    Determines whether an open position
    should be exited.
    """

    TAKE_PROFIT_PERCENT = 20.0
    STOP_LOSS_PERCENT = -10.0

    def analyze(
        self,
        position: PositionStatus,
    ) -> ExitDecision:

        # ------------------------
        # Take Profit
        # ------------------------

        if (
            position.return_percent
            >= self.TAKE_PROFIT_PERCENT
        ):
            return ExitDecision(
                should_exit=True,
                exit_type="TAKE_PROFIT",
                confidence=98,
                explanation=(
                    "Profit target reached."
                ),
            )

        # ------------------------
        # Stop Loss
        # ------------------------

        if (
            position.return_percent
            <= self.STOP_LOSS_PERCENT
        ):
            return ExitDecision(
                should_exit=True,
                exit_type="STOP_LOSS",
                confidence=99,
                explanation=(
                    "Stop loss reached."
                ),
            )

        # ------------------------
        # Weak Position
        # ------------------------

        if position.health == "WEAK":

            return ExitDecision(
                should_exit=False,
                exit_type="MONITOR",
                confidence=70,
                explanation=(
                    "Position is weak. "
                    "Continue monitoring."
                ),
            )

        return ExitDecision(
            should_exit=False,
            exit_type="HOLD",
            confidence=92,
            explanation=(
                "Position remains healthy."
            ),
        )


def main():

    manager = ExitManager()

    position = PositionStatus(
        health="STRONG",
        unrealized_pl=134.00,
        return_percent=20.62,
        stop_loss_active=True,
        take_profit_active=True,
    )

    decision = manager.analyze(position)

    print("\n====================================")
    print("STRATPILOT EXIT MANAGER")
    print("====================================")

    print(
        f"\nExit Decision    : "
        f"{decision.should_exit}"
    )

    print(
        f"Exit Type        : "
        f"{decision.exit_type}"
    )

    print(
        f"Confidence       : "
        f"{decision.confidence}/100"
    )

    print("\nExplanation")

    print(decision.explanation)

    print("\nThink First. Trade Second.")


if __name__ == "__main__":
    main()
