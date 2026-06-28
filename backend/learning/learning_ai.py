import json
import os


class LearningAI:

    def __init__(self):
        self.log_file = "logs/trade_journal.json"

    def learn(self):

        if not os.path.exists(self.log_file):
            return None

        with open(self.log_file, "r") as f:
            trades = json.load(f)

        lessons = []

        total = len(trades)

        approved = 0
        rejected = 0

        for trade in trades:

            commander = trade.get("commander", {})

            if commander.get("decision") == "TRADE APPROVED":
                approved += 1
            else:
                rejected += 1

        approval_rate = (
            approved / total * 100
            if total > 0 else 0
        )

        if approval_rate < 50:
            lessons.append(
                "System is rejecting most trades. Review entry conditions."
            )

        if rejected > approved:
            lessons.append(
                "Risk filters are protecting capital."
            )

        if total < 10:
            lessons.append(
                "Not enough historical data. Continue collecting trades."
            )

        return {
            "total": total,
            "approved": approved,
            "rejected": rejected,
            "approval_rate": round(approval_rate, 2),
            "lessons": lessons
        }


if __name__ == "__main__":

    ai = LearningAI()

    report = ai.learn()

    print("================================")
    print(" STRATPILOT LEARNING AI")
    print("================================")

    if report is None:
        print("No journal found.")
    else:

        print(f"Total Trades : {report['total']}")
        print(f"Approval %   : {report['approval_rate']}")

        print("\nLessons Learned")

        for lesson in report["lessons"]:
            print(f"- {lesson}")
