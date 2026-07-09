from decision.decision_engine import DecisionEngine
from risk.risk_manager import RiskManager
from execution.execution_guard import ExecutionGuard
from portfolio.portfolio_manager import PortfolioManager
from learning.continuous_learning import ContinuousLearningEngine


class DecisionValidator:

    def __init__(self):
        self.decision_engine = DecisionEngine()
        self.risk_manager = RiskManager()
        self.execution_guard = ExecutionGuard()
        self.portfolio_manager = PortfolioManager()
        self.learning_engine = ContinuousLearningEngine()

    def validate(self):
        decision = self.decision_engine.decide()
        risk = self.risk_manager.evaluate()
        guard = self.execution_guard.evaluate()
        portfolio = self.portfolio_manager.analyze()
        learning = self.learning_engine.evaluate()

        checks = []
        score = 0

        if decision["final_decision"] == "BUY":
            score += 20
            checks.append(("Decision Engine", "PASS", "BUY approved."))
        else:
            checks.append(("Decision Engine", "FAIL", "Decision is not BUY."))

        if risk["status"] == "APPROVED":
            score += 20
            checks.append(("Risk Manager", "PASS", "Risk approved."))
        else:
            checks.append(("Risk Manager", "FAIL", "Risk blocked trade."))

        if guard["execution"] == "SAFE TO EXECUTE":
            score += 20
            checks.append(("Execution Guard", "PASS", "Safe to execute."))
        else:
            checks.append(("Execution Guard", "FAIL", "Execution not approved."))

        allocation = portfolio["allocation"]

        if allocation["recommendation"] == "ALLOW":
            score += 20
            checks.append(("Portfolio Manager", "PASS", "Allocation allowed."))
        else:
            checks.append(("Portfolio Manager", "FAIL", "Allocation not allowed."))

        if learning["status"] != "REDUCE":
            score += 20
            checks.append(("Continuous Learning", "PASS", f"Learning status: {learning['status']}"))
        else:
            checks.append(("Continuous Learning", "FAIL", "Learning recommends reducing risk."))

        verdict = "VALIDATED" if score == 100 else "REVIEW REQUIRED"

        return {
            "score": score,
            "verdict": verdict,
            "checks": checks,
        }


if __name__ == "__main__":

    validator = DecisionValidator()
    report = validator.validate()

    print("\n====================================")
    print(" STRATPILOT DECISION VALIDATOR")
    print("====================================")

    print(f"Validation Score : {report['score']}")
    print(f"Final Verdict    : {report['verdict']}")

    print("\nChecks")
    print("------------------------------------")

    for name, status, reason in report["checks"]:
        print(f"{name}")
        print(f"Status : {status}")
        print(f"Reason : {reason}")
        print("------------------------------------")

    print("\nThink First. Trade Second.")
