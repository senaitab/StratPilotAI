from risk.risk_ai import RiskAI


class CommanderAI:
    def __init__(self):
        self.risk_ai = RiskAI()

    def analyze(self, option_price=None):
        risk = self.risk_ai.analyze()

        account_size = float(risk["account_size"])
        risk_percent = float(risk["risk_percent"])
        max_risk = float(risk["max_risk"])

        if option_price is None:
            option_price = 1.00

        option_price = float(option_price)

        contract_multiplier = 100
        contract_cost = option_price * contract_multiplier

        contracts = int(max_risk // contract_cost)

        capital_used = round(contracts * contract_cost, 2)

        risk_used_pct = round((capital_used / account_size) * 100, 2) if account_size > 0 else 0

        if contracts < 1:
            decision = "REJECTED"
            reason = "Option contract cost exceeds max risk."
        else:
            decision = "APPROVED"
            reason = "Position size is within risk limits."

        return {
            "account_size": account_size,
            "risk_percent": risk_percent,
            "max_risk": max_risk,
            "option_price": option_price,
            "contract_cost": round(contract_cost, 2),
            "contracts": contracts,
            "capital_used": capital_used,
            "risk_used_pct": risk_used_pct,
            "decision": decision,
            "reason": reason,
        }


if __name__ == "__main__":
    ai = PositionAI()

    test_prices = [0.25, 0.50, 1.00, 2.00]

    print("\n===================================")
    print("       STRATPILOT POSITION AI")
    print("===================================")

    for price in test_prices:
        report = ai.analyze(option_price=price)

        print(f"\nOption Price  : ${report['option_price']:.2f}")
        print(f"Contract Cost : ${report['contract_cost']:.2f}")
        print(f"Contracts     : {report['contracts']}")
        print(f"Capital Used  : ${report['capital_used']:.2f}")
        print(f"Risk Used     : {report['risk_used_pct']}%")
        print(f"Decision      : {report['decision']}")
        print(f"Reason        : {report['reason']}")

    print("\n===================================")
    print("Think First. Trade Second.")
