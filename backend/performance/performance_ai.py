import json
import os


class PerformanceAI:

    def __init__(self):
        self.log_file = "logs/trade_journal.json"

    def analyze(self):

        if not os.path.exists(self.log_file):
            return None

        with open(self.log_file, "r") as f:
            trades = json.load(f)

        total_trades = len(trades)

        approved = 0
        rejected = 0

        for trade in trades:

            commander = trade.get("commander", {})

            if commander.get("decision") == "TRADE APPROVED":
                approved += 1
            else:
                rejected += 1

        approval_rate = (
            approved / total_trades * 100
            if total_trades > 0
            else 0
        )

        return {
            "total": total_trades,
            "approved": approved,
            "rejected": rejected,
            "approval_rate": round(approval_rate, 2),
        }


if __name__ == "__main__":

    ai = PerformanceAI()

    report = ai.analyze()

    print("================================")
    print(" STRATPILOT PERFORMANCE AI")
    print("================================")

    if report is None:
        print("No journal found.")
    else:
        print(f"Total Decisions : {report['total']}")
        print(f"Approved        : {report['approved']}")
        print(f"Rejected        : {report['rejected']}")
        print(f"Approval Rate   : {report['approval_rate']}%")
