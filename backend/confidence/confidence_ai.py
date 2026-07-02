class ConfidenceAI:

    def calculate(self, report):

        confidence = 0

        # --------------------
        # Consensus
        # --------------------
        score = report.get("score", 0)
        confidence += score * 0.40

        # --------------------
        # Market Regime
        # --------------------
        regime = report.get("regime", "NORMAL")

        if regime == "BULL":
            confidence += 20

        elif regime == "RANGE":
            confidence += 15

        elif regime == "NORMAL":
            confidence += 12

        else:
            confidence += 8

        # --------------------
        # Risk
        # --------------------
        risk = report.get("risk_status", "SAFE")

        if risk == "SAFE":
            confidence += 20

        # --------------------
        # Strategy
        # --------------------
        strategy = report.get("strategy_confidence", 0)

        confidence += strategy * 20

        confidence = round(min(confidence, 100), 2)

        if confidence >= 90:
            level = "ELITE"

        elif confidence >= 80:
            level = "HIGH"

        elif confidence >= 70:
            level = "GOOD"

        elif confidence >= 60:
            level = "MODERATE"

        else:
            level = "LOW"

        return {
            "confidence": confidence,
            "level": level,
        }


if __name__ == "__main__":

    sample = {
        "score": 94.6,
        "regime": "RANGE",
        "risk_status": "SAFE",
        "strategy_confidence": 0.82,
    }

    ai = ConfidenceAI()

    result = ai.calculate(sample)

    print("\n==============================")
    print(" STRATPILOT CONFIDENCE AI")
    print("==============================")
    print(f"Confidence : {result['confidence']}")
    print(f"Level      : {result['level']}")
