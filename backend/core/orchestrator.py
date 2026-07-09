from decision.decision_engine import DecisionEngine
from risk.risk_manager import RiskManager
from execution.execution_guard import ExecutionGuard
from portfolio.portfolio_manager import PortfolioManager
from learning.continuous_learning import ContinuousLearningEngine
from validation.decision_validator import DecisionValidator
from execution.execution_simulator import ExecutionSimulator
from monitor.position_monitor import PositionMonitor


class StratPilotOrchestrator:

    def __init__(self):
        self.decision = DecisionEngine()
        self.risk = RiskManager()
        self.guard = ExecutionGuard()
        self.portfolio = PortfolioManager()
        self.learning = ContinuousLearningEngine()
        self.validator = DecisionValidator()
        self.simulator = ExecutionSimulator()
        self.monitor = PositionMonitor()

    def run(self):
        decision = self.decision.decide()
        risk = self.risk.evaluate()
        guard = self.guard.evaluate()
        portfolio = self.portfolio.analyze()
        learning = self.learning.evaluate()
        validator = self.validator.validate()

        ready = (
            decision["final_decision"] == "BUY"
            and risk["status"] == "APPROVED"
            and guard["status"] == "APPROVED"
            and portfolio["allocation"]["recommendation"] == "ALLOW"
            and learning["status"] != "REDUCE"
            and validator["verdict"] == "VALIDATED"
        )

        simulation = None
        monitor = None

        if ready:
            simulation = self.simulator.simulate()
            monitor = self.monitor.monitor()

        return {
            "ready": ready,
            "decision": decision,
            "risk": risk,
            "guard": guard,
            "portfolio": portfolio,
            "learning": learning,
            "validator": validator,
            "simulation": simulation,
            "monitor": monitor,
        }


if __name__ == "__main__":

    app = StratPilotOrchestrator()
    report = app.run()

    print("\n========================================")
    print("        STRATPILOT ORCHESTRATOR")
    print("========================================")

    print(f"Decision Engine     : {report['decision']['final_decision']}")
    print(f"Risk Manager        : {report['risk']['status']}")
    print(f"Execution Guard     : {report['guard']['execution']}")
    print(f"Portfolio Manager   : {report['portfolio']['allocation']['recommendation']}")
    print(f"Continuous Learning : {report['learning']['status']}")
    print(f"Decision Validator  : {report['validator']['verdict']}")

    print("\nSYSTEM STATUS")
    print("----------------------------------------")

    if report["ready"]:
        print("READY TO EXECUTE")

        if report["simulation"]:
            print(f"Simulation          : {report['simulation']['status']}")

        if report["monitor"]:
            print(f"Position Monitor    : {report['monitor']['recommendation']}")
    else:
        print("REVIEW REQUIRED")

    print("\nThink First. Trade Second.")
