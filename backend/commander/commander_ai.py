from consensus.consensus_ai import ConsensusAI


class CommanderAI:

    def __init__(self):
        self.consensus = ConsensusAI()

    def command(self, report):

        result = self.consensus.calculate(report)

        return {
            "decision": result["decision"],
            "score": result["score"],
            "grade": result["grade"],
            "confidence": result["confidence"],
            "breakdown": result["breakdown"],
        }


if __name__ == "__main__":

    sample = {

        "market": {
            "recommendation": "BUY"
        },

        "risk": {
            "status": "SAFE"
        },

        "strategy": {
            "confidence": 0.82
        },

        "options": {
            "decision": "BUY"
        },

        "position": {
            "decision": "ALLOW"
        },

        "portfolio": {
            "status": "HEALTHY"
        }

    }

    commander = CommanderAI()

    result = commander.command(sample)

    print("\n==============================")
    print(" STRATPILOT COMMANDER AI")
    print("==============================")

    print(f"Decision   : {result['decision']}")
    print(f"Score      : {result['score']}")
    print(f"Grade      : {result['grade']}")
    print(f"Confidence : {result['confidence']}")

    print("\nConsensus Breakdown")

    for name, pts in result["breakdown"].items():
        print(f"{name:<12}: {pts}")

    print("\nThink First. Trade Second.")
          
       
