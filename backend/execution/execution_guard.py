from decision.decision_engine import DecisionEngine
from risk.risk_manager import RiskManager
from sizing.position_sizer import PositionSizer


class ExecutionGuard:

    MIN_CONFIDENCE = 85

    def __init__(self):
        self.decision = DecisionEngine()
        self.risk = RiskManager()
        self.sizer = PositionSizer()

    def evaluate(self):
        decision = self.decision.decide()
        risk = self.risk.evaluate()
        sizing = self.sizer.calculate()

        commander = decision["commander"]
        market = decision["market"]

        checks = []
        blocked = False

        if market["market_status"] != "OPEN":
            blocked = True
            checks.append("✗ Market is not open.")
        else:
            checks.append("✓ Market is open.")

        if decision["final_decision"] != "BUY":
            blocked = True
            checks.append("✗ Decision Engine did not approve BUY.")
        else:
            checks.append("✓ Decision Engine approved BUY.")

        if commander["execution"]["status"] != "EXECUTE":
            blocked = True
            checks.append("✗ Commander execution not approved.")
        else:
            checks.append("✓ Commander execution approved.")

        if risk["status"] != "APPROVED":
            blocked = True
            checks.append("✗ Risk Manager blocked trade.")
        else:
            checks.append("✓ Risk Manager approved.")

        if sizing["contracts"] <= 0:
            blocked = True
            checks.append("✗ Invalid position size.")
        else:
            checks.append(f"✓ Position size: {sizing['contracts']} contract(s).")

        if sizing["confidence"] < self.MIN_CONFIDENCE:
            blocked = True
            checks.append("✗ Confidence below minimum.")
        else:
            checks.append(f"✓ Confidence: {sizing['confidence']:.2f}%.")

        if sizing["trade_grade"] not in ["A+", "A", "B"]:
            blocked = True
            checks.append("✗ Trade grade rejected.")
        else:
            checks.append(f"✓ Trade grade: {sizing['trade_grade']}.")

        status = "BLOCKED" if blocked else "APPROVED"
        execution = "DO NOT EXECUTE" if blocked else "SAFE TO EXECUTE"

        return {
            "status": status,
            "execution": execution,
            "checks": checks,
        }


if __name__ == "__main__":

    guard = ExecutionGuard()
    report = guard.evaluate()

    print("\n==============================")
    print(" STRATPILOT EXECUTION GUARD")
    print("==============================")

    print(f"Status     : {report['status']}")
    print(f"Execution  : {report['execution']}")

    print("\nChecks")
    print("------------------------------")
    for item in report["checks"]:
        print(item)

    print("\nThink First. Trade Second.")
