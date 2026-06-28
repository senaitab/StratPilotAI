from risk.risk_ai import RiskAI


class PositionAI:
    def __init__(self):
        self.risk_ai = RiskAI()

    def analyze(self, option_price=1.00):
        risk = self.risk_ai.analyze()

        account_size = float(risk["account_size"])
        risk_percent = float(risk["risk_percent"])
        max_risk = float(risk["max_risk"])

        contract_multiplier = 100
        contract_cost = option_price * contract_multiplier

        contracts = int(max_risk // contract_cost)

        if contracts < 1:
            decision = "REJECTED"
            reason = "Option contract cost exceeds max risk."
        else:
            decision = "APPROVED"
            reason = "Position size is within risk limits."

        capital_used = round(contracts * contract_cost, 2)

        if account_size > 0:
            risk_used_pct = round((capital_used / account_size) * 100, 2)
        else:
            risk_used_pct = 0

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

    # Test option price. Later OptionsAI will provide this.
    report = ai.analyze(option_price=1.00)

    print("\n===================================")
    print("       STRATPILOT POSITION AI")
    print("===================================")
    print(f"Account Size  : ${report['account_size']:.2f}")
    print(f"Risk Limit    : {report['risk_percent']}%")
    print(f"Max Risk      : ${report['max_risk']:.2f}")
    print("-----------------------------------")
    print(f"Option Price  : ${report['option_price']:.2f}")
    print(f"Contract Cost : ${report['contract_cost']:.2f}")
    print(f"Contracts     : {report['contracts']}")
    print(f"Capital Used  : ${report['capital_used']:.2f}")
    print(f"Risk Used     : {report['risk_used_pct']}%")
    print("-----------------------------------")
    print(f"Decision      : {report['decision']}")
    print(f"Reason        : {report['reason']}")
    print("===================================")
    print("Think First. Trade Second.")
