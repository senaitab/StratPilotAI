from execution.execution_gate import ExecutionGate


class ExecutionAI:

    def __init__(self):
        self.gate = ExecutionGate()

    def execute(self, report):
        gate = self.gate.evaluate(report)

        if not gate["execute"]:
            return {
                "status": "WAIT",
                "approved": False,
                "confidence": report.get("confidence", 0),
                "reasons": gate["reasons"],
            }

        return {
            "status": "EXECUTE",
            "approved": True,
            "confidence": report.get("confidence", 0),
            "reasons": gate["reasons"],
        }


if __name__ == "__main__":

    report = {
        "decision": "BUY",
        "confidence": 91.5,
        "risk_status": "SAFE",
        "position_status": "APPROVED",
        "portfolio_status": "HEALTHY",
        "regime": "BULL",
    }

    ai = ExecutionAI()

    result = ai.execute(report)

    print("\n==============================")
    print(" STRATPILOT EXECUTION AI")
    print("==============================")
    print(f"Status     : {result['status']}")
    print(f"Approved   : {result['approved']}")
    print(f"Confidence : {result['confidence']}")
    print()

    for reason in result["reasons"]:
        print("-", reason)
