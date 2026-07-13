from typing import Any, Dict, Optional

from decision.decision_engine import DecisionEngine
from risk.risk_manager import RiskManager
from execution.execution_guard import ExecutionGuard
from execution.execution_simulator import ExecutionSimulator
from portfolio.portfolio_manager import PortfolioManager
from learning.continuous_learning import ContinuousLearningEngine
from validation.decision_validator import DecisionValidator
from monitor.position_monitor import PositionMonitor
from feedback.trade_feedback import TradeFeedback
from state.state_manager import StateManager


class StratPilotOrchestrator:
    """
    Stage 26.6 — Automatic Feedback Pipeline

    Coordinates:
        Decision
        Risk
        Execution Guard
        Portfolio
        Continuous Learning
        Validation
        Simulation
        Position Monitoring
        Trade Feedback
        Shared State
    """

    def __init__(self) -> None:
        self.state = StateManager()

        self.decision_engine = DecisionEngine()
        self.risk_manager = RiskManager()
        self.execution_guard = ExecutionGuard()
        self.portfolio_manager = PortfolioManager()
        self.learning_engine = ContinuousLearningEngine()
        self.decision_validator = DecisionValidator()
        self.execution_simulator = ExecutionSimulator()
        self.position_monitor = PositionMonitor()
        self.trade_feedback = TradeFeedback()

    @staticmethod
    def _extract_contract(decision: Dict[str, Any]) -> Dict[str, Any]:
        """
        Safely extract the selected option contract from the
        DecisionEngine report.
        """
        best_contract = decision.get("best_contract", {})

        if not isinstance(best_contract, dict):
            return {}

        contract = best_contract.get("contract", {})

        return contract if isinstance(contract, dict) else {}

    @staticmethod
    def _extract_confidence(decision: Dict[str, Any]) -> float:
        """
        Safely read confidence from the current DecisionEngine structure.
        """
        commander = decision.get("commander", {})

        if not isinstance(commander, dict):
            return 0.0

        confidence_report = commander.get("confidence", {})

        if not isinstance(confidence_report, dict):
            return 0.0

        try:
            return float(confidence_report.get("confidence", 0.0))
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _extract_grade(decision: Dict[str, Any]) -> str:
        """
        Safely read the current trade grade.
        """
        commander = decision.get("commander", {})

        if not isinstance(commander, dict):
            return "UNKNOWN"

        consensus = commander.get("consensus", {})

        if not isinstance(consensus, dict):
            return "UNKNOWN"

        return str(consensus.get("grade", "UNKNOWN"))

    def _build_feedback_input(
        self,
        decision: Dict[str, Any],
        simulation: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Convert the current DecisionEngine and ExecutionSimulator outputs
        into the structure expected by TradeFeedback.process().
        """
        contract = self._extract_contract(decision)

        symbol = str(
            contract.get(
                "symbol",
                decision.get("market", {}).get("symbol", "UNKNOWN"),
            )
        )

        option_type = str(contract.get("type", "UNKNOWN"))
        grade = self._extract_grade(decision)

        strategy = f"{symbol}-{option_type}-{grade}"

        pnl_value = simulation.get(
            "realized_pnl",
            simulation.get(
                "profit_loss",
                simulation.get(
                    "pnl",
                    simulation.get("unrealized_pnl", 0.0),
                ),
            ),
        )

        try:
            profit_loss = float(pnl_value)
        except (TypeError, ValueError):
            profit_loss = 0.0

        return {
            "symbol": symbol,
            "strategy": strategy,
            "decision": decision.get("final_decision", "UNKNOWN"),
            "confidence": self._extract_confidence(decision),
            "profit_loss": profit_loss,
        }

    def run(self) -> Dict[str, Any]:
        # 1. Decision
        decision = self.decision_engine.decide()
        self.state.update("decision", decision)

        # 2. Risk
        risk = self.risk_manager.evaluate()
        self.state.update("risk", risk)

        # 3. Execution guard
        guard = self.execution_guard.evaluate()
        self.state.update("execution", guard)

        # 4. Portfolio
        portfolio = self.portfolio_manager.analyze()
        self.state.update("portfolio", portfolio)

        # 5. Current learning advice
        learning = self.learning_engine.evaluate()
        self.state.update("learning", learning)

        # 6. Final validation
        validation = self.decision_validator.validate()
        self.state.update("validation", validation)

        ready = (
            decision.get("final_decision") == "BUY"
            and risk.get("status") == "APPROVED"
            and guard.get("status") == "APPROVED"
            and portfolio.get("allocation", {}).get("recommendation") == "ALLOW"
            and learning.get("status") != "REDUCE"
            and validation.get("verdict") == "VALIDATED"
        )

        simulation: Optional[Dict[str, Any]] = None
        monitor: Optional[Dict[str, Any]] = None
        feedback: Optional[Dict[str, Any]] = None

        if ready:
            # 7. Simulated execution
            simulation = self.execution_simulator.simulate()
            self.state.update("simulation", simulation)

            # 8. Position monitoring
            monitor = self.position_monitor.monitor()
            self.state.update("monitor", monitor)

            # 9. Automatic trade feedback
            feedback_input = self._build_feedback_input(
                decision=decision,
                simulation=simulation,
            )

            feedback = self.trade_feedback.process(feedback_input)
            self.state.update("feedback", feedback)

        snapshot = self.state.snapshot()

        return {
            "ready": ready,
            "snapshot": snapshot,
            "decision": decision,
            "risk": risk,
            "guard": guard,
            "portfolio": portfolio,
            "learning": learning,
            "validation": validation,
            "simulation": simulation,
            "monitor": monitor,
            "feedback": feedback,
        }


def print_report(report: Dict[str, Any]) -> None:
    state = report.get("snapshot", {})

    decision = state.get("decision") or {}
    risk = state.get("risk") or {}
    execution = state.get("execution") or {}
    portfolio = state.get("portfolio") or {}
    learning = state.get("learning") or {}
    validation = state.get("validation") or {}

    print("\n========================================")
    print("       STRATPILOT UNIFIED PIPELINE")
    print("========================================")

    print(
        f"Decision      : "
        f"{decision.get('final_decision', 'UNKNOWN')}"
    )

    print(
        f"Risk          : "
        f"{risk.get('status', 'UNKNOWN')}"
    )

    print(
        f"Execution     : "
        f"{execution.get('execution', 'UNKNOWN')}"
    )

    print(
        f"Portfolio     : "
        f"{portfolio.get('allocation', {}).get('recommendation', 'UNKNOWN')}"
    )

    print(
        f"Learning      : "
        f"{learning.get('status', 'UNKNOWN')}"
    )

    print(
        f"Validation    : "
        f"{validation.get('verdict', 'UNKNOWN')}"
    )

    print("\nPipeline Status")
    print("----------------------------------------")

    if report.get("ready"):
        print("READY TO EXECUTE")
    else:
        print("REVIEW REQUIRED")

    simulation = report.get("simulation")

    if simulation:
        print(
            f"Simulation    : "
            f"{simulation.get('status', 'UNKNOWN')}"
        )

    monitor = report.get("monitor")

    if monitor:
        print(
            f"Monitor       : "
            f"{monitor.get('recommendation', 'UNKNOWN')}"
        )

    feedback = report.get("feedback")

    if feedback:
        print("\nTrade Feedback")
        print("----------------------------------------")
        print(f"Symbol        : {feedback.get('symbol', 'UNKNOWN')}")
        print(f"Strategy      : {feedback.get('strategy', 'UNKNOWN')}")
        print(f"Decision      : {feedback.get('decision', 'UNKNOWN')}")
        print(f"Confidence    : {feedback.get('confidence', 0)}%")
        print(f"Profit/Loss   : ${feedback.get('profit_loss', 0)}")
        print(f"Result        : {feedback.get('result', 'UNKNOWN')}")

    print("\nShared State")
    print("----------------------------------------")
    print(f"Last Updated  : {state.get('timestamp', 'UNKNOWN')}")

    print("\nThink First. Trade Second.")


if __name__ == "__main__":
    orchestrator = StratPilotOrchestrator()
    pipeline_report = orchestrator.run()
    print_report(pipeline_report)
