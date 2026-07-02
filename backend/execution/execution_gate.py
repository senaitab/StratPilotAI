class ExecutionGate:

    def evaluate(self, report):
        reasons = []

        if report.get("decision") != "BUY":
            reasons.append("Consensus is not BUY.")

        if report.get("confidence", 0) < 85:
            reasons.append("Confidence below threshold.")

        if report.get("risk_status") != "SAFE":
            reasons.append("Risk filter rejected.")

        if report.get("position_status") != "APPROVED":
            reasons.append("Position sizing rejected.")

        if report.get("portfolio_status") != "HEALTHY":
            reasons.append("Portfolio risk rejected.")

        regime = report.get("regime")

        if regime not in ("BULL", "RANGE", "NORMAL"):
            reasons.append("Market regime not tradable.")

        if reasons:
            return {
                "execute": False,
                "status": "WAIT",
                "reasons": reasons,
            }

        return {
            "execute": True,
            "status": "EXECUTE",
            "reasons": ["All execution checks passed."],
        }


if __name__ == "__main__":

    sample = {
        "decision": "BUY",
        "confidence": 89.24,
        "risk_status": "SAFE",
        "position_status": "APPROVED",
        "portfolio_status": "HEALTHY",
        "regime": "RANGE",
    }

    gate = ExecutionGate()
    result = gate.evaluate(sample)

    print("\n==============================")
    print(" STRATPILOT EXECUTION GATE")
    print("==============================")
    print(f"Status : {result['status']}")
    print()

    for r in result["reasons"]:
        print("-", r)
