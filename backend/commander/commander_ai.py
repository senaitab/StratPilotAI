from consensus.consensus_ai import ConsensusAI
from regime.regime_ai import RegimeAI
from consensus.weights import DynamicWeights


class CommanderAI:

    def __init__(self):
        self.consensus = ConsensusAI()
        self.regime = RegimeAI()
        self.weights = DynamicWeights()

    def command(self, report):
        market = report.get("market", {})

        regime = self.regime.detect(market)
        weights = self.weights.get(regime)

        result = self.consensus.calculate(report)

        return {
            "regime": regime,
            "weights": weights,
            "decision": result["decision"],
            "score": result["score"],
            "grade": result["grade"],
            "confidence": result["confidence"],
            "breakdown": result["breakdown"],
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
        },
        "portfolio": {
            "status": "HEALTHY",
        },
    }

    commander = CommanderAI()
    result = commander.command(sample)

    print("\n==============================")
    print(" STRATPILOT COMMANDER AI")
    print("==============================")

    print("\nMarket Regime")
    print("------------------------------")
    print(result["regime"])

    print("\nDynamic Weights")
    print("------------------------------")
    for name, weight in result["weights"].items():
        print(f"{name:<12}: {weight}")

    print("\nConsensus")
    print("------------------------------")
    print(f"Decision   : {result['decision']}")
    print(f"Score      : {result['score']}")
    print(f"Grade      : {result['grade']}")
    print(f"Confidence : {result['confidence']}")

    print("\nConsensus Breakdown")
    print("------------------------------")
    for name, pts in result["breakdown"].items():
        print(f"{name:<12}: {pts}")

    print("\nThink First. Trade Second.")
          
       
