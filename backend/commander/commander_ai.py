from consensus.consensus_ai import ConsensusAI
from regime.regime_ai import RegimeAI
from consensus.weights import DynamicWeights
from confidence.confidence_ai import ConfidenceAI
from execution.execution_ai import ExecutionAI


class CommanderAI:

    def __init__(self):
        self.consensus = ConsensusAI()
        self.regime = RegimeAI()
        self.weights = DynamicWeights()
        self.confidence = ConfidenceAI()
        self.execution = ExecutionAI()

    def command(self, report):
        market = report.get("market", {})
        risk = report.get("risk", {})
        strategy = report.get("strategy", {})
        position = report.get("position", {})
        portfolio = report.get("portfolio", {})

        regime = self.regime.detect(market)
        weights = self.weights.get(regime)

        consensus = self.consensus.calculate(report, weights)

        confidence = self.confidence.calculate({
            "score": consensus["score"],
            "regime": regime,
            "risk_status": risk.get("status", "SAFE"),
            "strategy_confidence": strategy.get("confidence", 0),
        })

        execution = self.execution.execute({
            "decision": consensus["decision"],
            "confidence": confidence["confidence"],
            "risk_status": risk.get("status", "SAFE"),
            "position_status": position.get("status", "APPROVED"),
            "portfolio_status": portfolio.get("status", "HEALTHY"),
            "regime": regime,
        })

        return {
            "regime": regime,
            "weights": weights,
            "consensus": consensus,
            "confidence": confidence,
            "execution": execution,
        }


if __name__ == "__main__":

    sample = {
        "market": {
            "change_pct": 0.05,
            "recommendation": "BUY",
        },
        "risk": {
            "status": "SAFE",
        },
        "strategy": {
            "confidence": 0.82,
        },
        "options": {
            "decision": "BUY",
        },
        "position": {
            "decision": "ALLOW",
            "status": "APPROVED",
        },
        "portfolio": {
            "status": "HEALTHY",
        },
    }

    commander = CommanderAI()
    report = commander.command(sample)

    print("\n==============================")
    print(" STRATPILOT COMMANDER AI")
    print("==============================")

    print(f"Regime      : {report['regime']}")
    print(f"Decision    : {report['consensus']['decision']}")
    print(f"Score       : {report['consensus']['score']}")
    print(f"Grade       : {report['consensus']['grade']}")
    print(f"Confidence  : {report['confidence']['confidence']}")
    print(f"Level       : {report['confidence']['level']}")
    print(f"Execution   : {report['execution']['status']}")
    print(f"Approved    : {report['execution']['approved']}")

    print("\nExecution Reasons")
    print("------------------------------")
    for reason in report["execution"]["reasons"]:
        print("-", reason)

    print("\nThink First. Trade Second.")
