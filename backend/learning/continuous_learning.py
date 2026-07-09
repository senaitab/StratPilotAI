from learning.adaptive_learning import AdaptiveLearningEngine


class ContinuousLearningEngine:

    def __init__(self):
        self.learning = AdaptiveLearningEngine()

    def evaluate(self):

        result = self.learning.analyze()

        if result["status"] != "READY":
            return {
                "status": "NO DATA",
                "message": "No learning data available."
            }

        best = result["best_setup"]
        stats = result["report"][best]

        count = stats["count"]
        win_rate = stats["win_rate"]
        confidence = stats["average_confidence"]
        profit = stats["net_profit"]

        if count < 5:
            status = "LEARNING"
            adjustment = 0
            reason = "Not enough completed trades."

        elif profit <= 0:
            status = "REDUCE"
            adjustment = -2
            reason = "Historical profitability is negative."

        elif win_rate >= 70:
            status = "BOOST"
            adjustment = 3
            reason = "Excellent historical performance."

        elif win_rate >= 60:
            status = "BOOST"
            adjustment = 1
            reason = "Consistent historical performance."

        elif win_rate >= 50:
            status = "NEUTRAL"
            adjustment = 0
            reason = "Maintain current weighting."

        else:
            status = "REDUCE"
            adjustment = -2
            reason = "Historical performance is below target."

        return {

            "status": status,
            "setup": best,
            "count": count,
            "win_rate": win_rate,
            "confidence": confidence,
            "net_profit": profit,
            "adjustment": adjustment,
            "reason": reason

        }


if __name__ == "__main__":

    engine = ContinuousLearningEngine()

    report = engine.evaluate()

    print("\n================================")
    print(" STRATPILOT CONTINUOUS LEARNING")
    print("================================")

    if report["status"] == "NO DATA":

        print(report["message"])

    else:

        print(f"Learning Status      : {report['status']}")
        print(f"Historical Setup     : {report['setup']}")
        print(f"Completed Trades     : {report['count']}")
        print(f"Win Rate             : {report['win_rate']}%")
        print(f"Average Confidence   : {report['confidence']}%")
        print(f"Net Profit           : ${report['net_profit']}")
        print(f"Confidence Adjustment: {report['adjustment']}")

        print("\nRecommendation")
        print("--------------------------------")
        print(report["reason"])

    print("\nThink First. Trade Second.")
