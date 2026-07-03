from portfolio.portfolio_adapter import PortfolioAdapter
from sizing.position_sizer import PositionSizer


class RiskManager:

    MAX_DAILY_LOSS = -500
    MAX_OPEN_POSITIONS = 5
    MIN_CONFIDENCE = 85

    def __init__(self):
        self.portfolio = PortfolioAdapter()
        self.sizer = PositionSizer()

    def evaluate(self):

        account = self.portfolio.snapshot()
        sizing = self.sizer.calculate()

        checks = []
        blocked = False
        score = 100

        # ----------------------------------
        # Portfolio Health
        # ----------------------------------

        if account["equity"] <= 0:
            blocked = True
            score -= 50
            checks.append("✗ Account equity invalid.")
        else:
            checks.append("✓ Portfolio healthy.")

        # ----------------------------------
        # Buying Power
        # ----------------------------------

        if sizing["capital_required"] > account["buying_power"]:
            blocked = True
            score -= 20
            checks.append("✗ Insufficient buying power.")
        else:
            checks.append("✓ Buying power available.")

        # ----------------------------------
        # Daily Loss
        # ----------------------------------

        if account["daily_pnl"] <= self.MAX_DAILY_LOSS:
            blocked = True
            score -= 25
            checks.append("✗ Daily loss limit exceeded.")
        else:
            checks.append("✓ Daily loss within limit.")

        # ----------------------------------
        # Open Positions
        # ----------------------------------

        if account["open_positions"] >= self.MAX_OPEN_POSITIONS:
            blocked = True
            score -= 15
            checks.append("✗ Maximum open positions reached.")
        else:
            checks.append(
                f"✓ Open positions: {account['open_positions']}/{self.MAX_OPEN_POSITIONS}"
            )

        # ----------------------------------
        # Confidence
        # ----------------------------------

        if sizing["confidence"] < self.MIN_CONFIDENCE:
            blocked = True
            score -= 20
            checks.append("✗ Confidence below threshold.")
        else:
            checks.append(
                f"✓ Confidence: {sizing['confidence']:.2f}%"
            )

        # ----------------------------------
        # Position Size
        # ----------------------------------

        if sizing["contracts"] <= 0:
            blocked = True
            score -= 20
            checks.append("✗ Position size rejected.")
        else:
            checks.append(
                f"✓ Position size: {sizing['contracts']} contract(s)"
            )

        # ----------------------------------
        # Contract Quality
        # ----------------------------------

        if sizing["trade_grade"] not in ["A+", "A", "B"]:
            blocked = True
            score -= 10
            checks.append("✗ Trade quality too low.")
        else:
            checks.append(
                f"✓ Trade grade: {sizing['trade_grade']}"
            )

        score = max(0, min(score, 100))

        if score >= 95:
            risk_level = "LOW"
        elif score >= 80:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        status = "APPROVED" if not blocked else "BLOCKED"

        return {
            "status": status,
            "risk_score": score,
            "risk_level": risk_level,
            "checks": checks,
        }


if __name__ == "__main__":

    manager = RiskManager()

    report = manager.evaluate()

    print("\n==============================")
    print(" STRATPILOT RISK MANAGER")
    print("==============================")

    print(f"Status      : {report['status']}")
    print(f"Risk Score  : {report['risk_score']}")
    print(f"Risk Level  : {report['risk_level']}")

    print("\nChecks")
    print("------------------------------")

    for check in report["checks"]:
        print(check)

    print("\nThink First. Trade Second.")
