from risk.risk_ai import RiskAI


class PortfolioAI:
    def __init__(self):
        self.risk_ai = RiskAI()

    def analyze(self):
        risk = self.risk_ai.analyze()

        account_size = float(risk["account_size"])
        max_risk = float(risk["max_risk"])

        open_positions = 0
        portfolio_risk = 0.0
        cash_available = account_size

        if account_size < 100:
            status = "LIMITED"
            recommendation = "WAIT"
            reason = "Account size is too small for safe portfolio expansion."
        elif max_risk < 5:
            status = "LIMITED"
            recommendation = "WAIT"
            reason = "Available risk budget is too small."
        else:
            status = "HEALTHY"
            recommendation = "ALLOW NEW TRADE"
            reason = "Portfolio has enough available risk."

        return {
            "account_size": account_size,
            "cash_available": cash_available,
            "open_positions": open_positions,
            "portfolio_risk": portfolio_risk,
            "max_risk": max_risk,
            "status": status,
            "recommendation": recommendation,
            "reason": reason,
        }


if __name__ == "__main__":
    ai = PortfolioAI()
    report = ai.analyze()

    print("\n===================================")
    print("      STRATPILOT PORTFOLIO AI")
    print("===================================")
    print(f"Account Size   : ${report['account_size']:.2f}")
    print(f"Cash Available : ${report['cash_available']:.2f}")
    print(f"Open Positions : {report['open_positions']}")
    print(f"Max Risk       : ${report['max_risk']:.2f}")
    print(f"Portfolio Risk : {report['portfolio_risk']}%")
    print("-----------------------------------")
    print(f"Status         : {report['status']}")
    print(f"Recommendation : {report['recommendation']}")
    print(f"Reason         : {report['reason']}")
    print("===================================")
    print("Think First. Trade Second.")
