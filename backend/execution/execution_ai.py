from ai.commander_ai import CommanderAI


class ExecutionAI:
    def __init__(self):
        self.commander = CommanderAI()

    def execute(self):
        report = self.commander.analyze()

        if report["decision"] != "TRADE APPROVED":
            return {
                "status": "NOT READY",
                "reason": "CommanderAI rejected trade.",
                "report": report,
            }

        return {
            "status": "READY",
            "ticker": report.get("ticker", "SPY"),
            "direction": report.get("contract", "CALL"),
            "contracts": report.get("contracts", 1),
            "limit_price": report.get("price", 0.00),
            "reason": "All AI systems approved.",
        }


if __name__ == "__main__":
    ai = ExecutionAI()

    result = ai.execute()

    print("\n===================================")
    print("      STRATPILOT EXECUTION AI")
    print("===================================")

    print(f"Status : {result['status']}")

    if result["status"] == "READY":
        print(f"Ticker      : {result['ticker']}")
        print(f"Direction   : {result['direction']}")
        print(f"Contracts   : {result['contracts']}")
        print(f"Limit Price : ${result['limit_price']}")
    else:
        print(f"Reason : {result['reason']}")

    print("===================================")
    print("Think First. Trade Second.")
