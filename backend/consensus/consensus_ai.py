class ConsensusAI:

    def calculate(self, report, weights):

        score = 0
        breakdown = {}

        market = report.get("market", {})
        if market.get("recommendation") == "BUY":
            pts = weights["market"]
        elif market.get("recommendation") == "WAIT":
            pts = weights["market"] * 0.50
        else:
            pts = 0
        breakdown["market"] = pts
        score += pts

        risk = report.get("risk", {})
        if risk.get("status") != "NO TRADE":
            pts = weights["risk"]
        else:
            pts = 0
        breakdown["risk"] = pts
        score += pts

        strategy = report.get("strategy", {})
        confidence = strategy.get("confidence", 0)
        pts = confidence * weights["strategy"]
        breakdown["strategy"] = round(pts, 2)
        score += pts

        options = report.get("options", {})
        if options.get("decision") == "BUY":
            pts = weights["options"]
        else:
            pts = 0
        breakdown["options"] = pts
        score += pts

        position = report.get("position", {})
        if position.get("decision") != "REJECTED":
            pts = weights["position"]
        else:
            pts = 0
        breakdown["position"] = pts
        score += pts

        portfolio = report.get("portfolio", {})
        if portfolio.get("status") == "HEALTHY":
            pts = weights["portfolio"]
        else:
            pts = 0
        breakdown["portfolio"] = pts
        score += pts

        score = round(score, 2)

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

    sample_report = {
        "market": {"recommendation": "BUY"},
        "risk": {"status": "SAFE"},
        "strategy": {"confidence": 0.82},
        "options": {"decision": "BUY"},
        "position": {"decision": "ALLOW"},
        "portfolio": {"status": "HEALTHY"},
    }

    sample_weights = {
        "market": 20,
        "risk": 25,
        "strategy": 30,
        "options": 10,
        "position": 10,
        "portfolio": 5,
    }

    ai = ConsensusAI()
    result = ai.calculate(sample_report, sample_weights)

    print("\n==============================")
    print(" STRATPILOT CONSENSUS AI")
    print("==============================")
    print(f"Decision   : {result['decision']}")
    print(f"Score      : {result['score']}")
    print(f"Grade      : {result['grade']}")
    print(f"Confidence : {result['confidence']}")

    print("\nBreakdown")
    for name, pts in result["breakdown"].items():
        print(f"{name:<12}: {pts}")
      

      
