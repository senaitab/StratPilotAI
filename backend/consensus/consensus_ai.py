class ConsensusAI:

    def __init__(self):
        self.weights = {
            "market": 30,
            "risk": 25,
            "strategy": 20,
            "options": 10,
            "position": 10,
            "portfolio": 5,
        }

    def calculate(self, report):

        score = 0
        breakdown = {}

        # --------------------------
        # MARKET
        # --------------------------

        market = report.get("market", {})

        if market.get("recommendation") == "BUY":
            pts = self.weights["market"]

        elif market.get("recommendation") == "WAIT":
            pts = self.weights["market"] * 0.50

        else:
            pts = 0

        breakdown["market"] = pts
        score += pts

        # --------------------------
        # RISK
        # --------------------------

        risk = report.get("risk", {})

        if risk.get("status") != "NO TRADE":
            pts = self.weights["risk"]
        else:
            pts = 0

        breakdown["risk"] = pts
        score += pts

        # --------------------------
        # STRATEGY
        # --------------------------

        strategy = report.get("strategy", {})

        confidence = strategy.get("confidence", 0)

        pts = confidence * self.weights["strategy"]

        breakdown["strategy"] = round(pts, 2)

        score += pts

        # --------------------------
        # OPTIONS
        # --------------------------

        options = report.get("options", {})

        if options.get("decision") == "BUY":
            pts = self.weights["options"]
        else:
            pts = 0

        breakdown["options"] = pts
        score += pts

        # --------------------------
        # POSITION
        # --------------------------

        position = report.get("position", {})

        if position.get("decision") != "REJECTED":
            pts = self.weights["position"]
        else:
            pts = 0

        breakdown["position"] = pts
        score += pts

        # --------------------------
        # PORTFOLIO
        # --------------------------

        portfolio = report.get("portfolio", {})

        if portfolio.get("status") == "HEALTHY":
            pts = self.weights["portfolio"]
        else:
            pts = 0

        breakdown["portfolio"] = pts
        score += pts

        score = round(score, 2)

        # --------------------------
        # Grade
        # --------------------------

        if score >= 85:
            grade = "A"
            decision = "BUY"

        elif score >= 70:
            grade = "B"
            decision = "BUY"

        elif score >= 55:
            grade = "C"
            decision = "WAIT"

        else:
            grade = "D"
            decision = "WAIT"

        return {
            "score": score,
            "grade": grade,
            "decision": decision,
            "confidence": round(score / 100, 2),
            "breakdown": breakdown,
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
            "confidence": 0.83
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

    ai = ConsensusAI()

    result = ai.calculate(sample)

    print("\n==============================")
    print(" STRATPILOT CONSENSUS AI")
    print("==============================")

    print(f"Score      : {result['score']}")
    print(f"Grade      : {result['grade']}")
    print(f"Decision   : {result['decision']}")
    print(f"Confidence : {result['confidence']}")

    print("\nBreakdown")

    for k, v in result["breakdown"].items():
        print(f"{k:<12}: {v}")

      
