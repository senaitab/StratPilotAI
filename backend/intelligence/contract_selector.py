from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class OptionContract:
    symbol: str
    option_type: str
    strike: float
    expiration: str
    delta: float
    bid: float
    ask: float
    volume: int
    open_interest: int


@dataclass(frozen=True)
class ContractSelectionResult:
    contract: OptionContract
    liquidity_score: int
    overall_score: int
    explanation: str


class ContractSelector:
    """
    Stage 32.3

    Selects the highest quality option
    contract from a list of candidates.
    """

    TARGET_DELTA = 0.40

    def _score_contract(
        self,
        contract: OptionContract,
    ) -> int:

        score = 0

        # ----------------------
        # Delta
        # ----------------------

        delta_diff = abs(contract.delta - self.TARGET_DELTA)

        score += max(0, 40 - int(delta_diff * 100))

        # ----------------------
        # Spread
        # ----------------------

        spread = contract.ask - contract.bid

        if spread <= 0.03:
            score += 25

        elif spread <= 0.08:
            score += 15

        # ----------------------
        # Volume
        # ----------------------

        if contract.volume >= 1000:
            score += 20

        elif contract.volume >= 500:
            score += 10

        # ----------------------
        # Open Interest
        # ----------------------

        if contract.open_interest >= 1000:
            score += 15

        elif contract.open_interest >= 500:
            score += 8

        return score

    def analyze(
        self,
        contracts: List[OptionContract],
    ) -> ContractSelectionResult:

        best = max(
            contracts,
            key=self._score_contract,
        )

        score = self._score_contract(best)

        liquidity = min(
            100,
            int(
                (
                    best.volume
                    + best.open_interest
                )
                / 200
            ),
        )

        return ContractSelectionResult(
            contract=best,
            liquidity_score=liquidity,
            overall_score=score,
            explanation=(
                "Highest overall contract score "
                "based on liquidity, spread, "
                "and delta alignment."
            ),
        )


def main():

    contracts = [

        OptionContract(
            symbol="SPY",
            option_type="CALL",
            strike=650,
            expiration="2026-07-24",
            delta=0.41,
            bid=2.20,
            ask=2.23,
            volume=6400,
            open_interest=12000,
        ),

        OptionContract(
            symbol="SPY",
            option_type="CALL",
            strike=651,
            expiration="2026-07-24",
            delta=0.21,
            bid=1.40,
            ask=1.50,
            volume=250,
            open_interest=300,
        ),

        OptionContract(
            symbol="SPY",
            option_type="CALL",
            strike=649,
            expiration="2026-07-24",
            delta=0.52,
            bid=3.00,
            ask=3.06,
            volume=1800,
            open_interest=4200,
        ),

    ]

    selector = ContractSelector()

    result = selector.analyze(contracts)

    print("\n====================================")
    print("STRATPILOT CONTRACT SELECTOR")
    print("====================================")

    c = result.contract

    print(f"\n Selected Contract")

    print(
        f" {c.symbol} "
        f"{int(c.strike)} "
        f"{c.option_type}"
    )

    print(f"\n Expiration")

    print(f" {c.expiration}")

    print(f"\n Delta")

    print(f" {c.delta:.2f}")

    print(f"\n Liquidity Score")

    print(
        f" {result.liquidity_score}/100"
    )

    print(f"\n Overall Score")

    print(
        f" {result.overall_score}/100"
    )

    print("\n Explanation")

    print(result.explanation)

    print("\n Think First. Trade Second.")


if __name__ == "__main__":
    main()
