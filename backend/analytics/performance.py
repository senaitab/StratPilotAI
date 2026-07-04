import json
from pathlib import Path


class PerformanceAnalytics:

    def __init__(self):
        self.file = Path("trade_history.json")

    def analyze(self):

        if not self.file.exists():
            return None

        with open(self.file, "r") as f:
            trades = json.load(f)

        total = len(trades)

        if total == 0:
            return None

        confidence = 0
        grade_count = {}

        decisions = {}

        for trade in trades:

            confidence += trade.get("confidence", 0)

            grade = trade.get("trade_grade", "N/A")
            grade_count[grade] = grade_count.get(grade, 0) + 1

            decision = trade.get("decision", "UNKNOWN")
            decisions[decision] = decisions.get(decision, 0) + 1

        avg_confidence = round(confidence / total, 2)

        best_grade = max(
            grade_count,
            key=grade_count.get
        )

        return {
            "total_trades": total,
            "average_confidence": avg_confidence,
            "best_grade": best_grade,
            "decision_breakdown": decisions,
            "grade_breakdown": grade_count
        }


if __name__ == "__main__":

    analytics = PerformanceAnalytics()

    report = analytics.analyze()

    print()

    print("==============================")
    print(" STRATPILOT PERFORMANCE")
    print("==============================")

    if report is None:

        print("No trades recorded.")

    else:

        print(f"Trades              : {report['total_trades']}")
        print(f"Average Confidence  : {report['average_confidence']}%")
        print(f"Most Common Grade   : {report['best_grade']}")

        print()

        print("Decision Breakdown")
        print("------------------------------")

        for k, v in report["decision_breakdown"].items():
            print(f"{k:<10} {v}")

        print()

        print("Grade Breakdown")
        print("------------------------------")

        for k, v in report["grade_breakdown"].items():
            print(f"{k:<10} {v}")

    print()
    print("Think First. Trade Second.")
