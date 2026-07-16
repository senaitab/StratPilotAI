from dataclasses import dataclass


@dataclass
class RiskDecision:
    account_size: float
    risk_percent: float
    dollar_risk: float
    contracts: int
    risk_level: str
    recommendation: str


class RiskEngine:

    def evaluate(
        self,
        account_size: float,
        confidence: int,
        volatility: int,
        option_risk_per_contract: float,
    ) -> RiskDecision:

        # Base risk percentage
        risk_percent = 0.005  # 0.5%

        # Reduce risk if confidence is lower
        if confidence < 85:
            risk_percent *= 0.75

        # Reduce risk again if volatility is elevated
        if volatility > 85:
            risk_percent *= 0.75

        dollar_risk = account_size * risk_percent

        contracts = max(
            1,
            int(dollar_risk // option_risk_per_contract)
        )

        if risk_percent >= 0.005:
            risk_level = "LOW"

        elif risk_percent >= 0.003:
            risk_level = "MEDIUM"

        else:
            risk_level = "HIGH"

        recommendation = (
            "APPROVED"
            if confidence >= 75
            else "REDUCE SIZE"
        )

        return RiskDecision(
            account_size,
            risk_percent,
            dollar_risk,
            contracts,
            risk_level,
            recommendation,
        )


if __name__ == "__main__":

    engine = RiskEngine()

    result = engine.evaluate(
        account_size=10000,
        confidence=78,
        volatility=81,
        option_risk_per_contract=50,
    )

    print("\n===================================")
    print("STRATPILOT RISK ENGINE")
    print("===================================")

    print(f"Account Size      : ${result.account_size:,.2f}")
    print(f"Risk %            : {result.risk_percent*100:.2f}%")
    print(f"Dollar Risk       : ${result.dollar_risk:.2f}")
    print(f"Contracts         : {result.contracts}")
    print(f"Risk Level        : {result.risk_level}")
    print(f"Recommendation    : {result.recommendation}")

    print("\nThink First. Trade Second.")
