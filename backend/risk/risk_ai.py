from broker.webull_client import WebullClient


class RiskAI:
    """
    RiskAI protects the account before any trade is allowed.
    """

    def __init__(self):
        self.client = WebullClient()

    def analyze(self):
        balance = self.client.get_balance()

        net_liq = float(balance["total_net_liquidation_value"])

        max_risk_percent = 1.0
        max_risk_dollars = round(net_liq * (max_risk_percent / 100), 2)

        if max_risk_dollars < 5:
            status = "NO TRADE"
            reason = "Account too small for defined risk."
        else:
            status = "APPROVED"
            reason = "Risk within limits."

        return {
            "account_size": net_liq,
            "risk_percent": max_risk_percent,
            "max_risk": max_risk_dollars,
            "status": status,
            "reason": reason,
        }


if __name__ == "__main__":
    ai = RiskAI()
    report = ai.analyze()

    print("\n===================================")
    print("        STRATPILOT RISK AI")
    print("===================================")
    print(f"Account Size : ${report['account_size']:.2f}")
    print(f"Risk Limit   : {report['risk_percent']}%")
    print(f"Max Risk     : ${report['max_risk']:.2f}")
    print(f"Decision     : {report['status']}")
    print(f"Reason       : {report['reason']}")
    print("===================================")
