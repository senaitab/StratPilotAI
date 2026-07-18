from dataclasses import dataclass


@dataclass(frozen=True)
class RiskResult:
    risk_level: str
    risk_multiplier: float
    trade_allowed: bool
    explanation: str


@dataclass(frozen=True)
class PositionSizeResult:
    account_balance: float
    base_risk_percent: float
    effective_risk_percent: float
    risk_amount: float
    risk_per_contract: float
    contracts: int
    explanation: str


class PositionSizer:
    """
    Stage 32.2

    Converts approved trade risk into
    the number of option contracts.
    """

    def analyze(
        self,
        account_balance: float,
        base_risk_percent: float,
        risk_result: RiskResult,
        risk_per_contract: float,
    ) -> PositionSizeResult:

        if account_balance <= 0:
            raise ValueError("Account balance must be positive.")

        if risk_per_contract <= 0:
            raise ValueError(
                "Risk per contract must be positive."
            )

        if not risk_result.trade_allowed:

            return PositionSizeResult(
                account_balance=account_balance,
                base_risk_percent=base_risk_percent,
                effective_risk_percent=0.0,
                risk_amount=0.0,
                risk_per_contract=risk_per_contract,
                contracts=0,
                explanation=(
                    "Trade not approved. "
                    "Position size is zero."
                ),
            )

        effective_risk_percent = (
            base_risk_percent
            * risk_result.risk_multiplier
        )

        risk_amount = (
            account_balance
            * effective_risk_percent
            / 100.0
        )

        contracts = max(
            1,
            int(
                risk_amount
                // risk_per_contract
            ),
        )

        return PositionSizeResult(
            account_balance=account_balance,
            base_risk_percent=base_risk_percent,
            effective_risk_percent=effective_risk_percent,
            risk_amount=risk_amount,
            risk_per_contract=risk_per_contract,
            contracts=contracts,
            explanation=(
                "Dynamic position size calculated "
                "using approved account risk."
            ),
        )


def main():

    risk = RiskResult(
        risk_level="MEDIUM",
        risk_multiplier=0.50,
        trade_allowed=True,
        explanation="Good setup.",
    )

    sizer = PositionSizer()

    result = sizer.analyze(
        account_balance=10000,
        base_risk_percent=1.0,
        risk_result=risk,
        risk_per_contract=25,
    )

    print("\n====================================")
    print("STRATPILOT POSITION SIZER")
    print("====================================")

    print(
        f" Account Balance     : "
        f"${result.account_balance:,.2f}"
    )

    print(
        f" Base Risk           : "
        f"{result.base_risk_percent:.2f}%"
    )

    print(
        f" Effective Risk      : "
        f"{result.effective_risk_percent:.2f}%"
    )

    print(
        f" Risk Amount         : "
        f"${result.risk_amount:.2f}"
    )

    print(
        f" Risk Per Contract   : "
        f"${result.risk_per_contract:.2f}"
    )

    print(
        f" Contracts           : "
        f"{result.contracts}"
    )

    print("\n Explanation")
    print(result.explanation)

    print("\n Think First. Trade Second.")


if __name__ == "__main__":
    main()
