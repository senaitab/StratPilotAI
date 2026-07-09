import json
from pathlib import Path


class AdaptiveLearningEngine:

    def __init__(self):
        self.history_file = Path("trade_history.json")

    def load_history(self):

        if not self.history_file.exists():
            return []

        try:
            with open(self.history_file, "r") as f:
                return json.load(f)
        except Exception:
            return []

    def analyze(self):

        trades = self.load_history()

        if not trades:

            return {
                "status": "NO DATA",
                "message": "No completed trades available.",
            }

        setups = {}

        for trade in trades:

            key = (
                f"{trade.get('symbol','?')}-"
                f"{trade.get('type','?')}-"
                f"{trade.get('trade_grade','?')}"
            )

            if key not in setups:
                setups[key] = {
                    "count": 0,
                    "wins": 0,
                    "losses": 0,
                    "confidence": 0,
                    "profit": 0,
                }

            pnl = float(
                trade.get(
                    "realized_pnl",
                    trade.get("pnl", 0)
                )
            )

            setups[key]["count"] += 1
            setups[key]["confidence"] += trade.get(
                "confidence",
                0
            )

            setups[key]["profit"] += pnl

            if pnl > 0:
                setups[key]["wins"] += 1
            elif pnl < 0:
                setups[key]["losses"] += 1

        report = {}

        for key, data in setups.items():

            count = data["count"]

            report[key] = {

                "count": count,

                "average_confidence": round(
                    data["confidence"] / count,
                    2,
                ),

                "win_rate": round(
                    (data["wins"] / count) * 100,
                    2,
                ),

                "net_profit": round(
                    data["profit"],
                    2,
                ),
            }

        best_setup = max(
            report,
            key=lambda x: (
                report[x]["net_profit"],
                report[x]["win_rate"],
                report[x]["average_confidence"],
            ),
        )

        recommendation = self.recommend(report[best_setup])

        return {

            "status": "READY",

            "trades": len(trades),

            "best_setup": best_setup,

            "report": report,

            "recommendation": recommendation,
        }

    def recommend(self, setup):

        if setup["count"] < 5:
            return (
                "LEARNING MODE: "
                "Collect additional completed trades."
            )

        if (
            setup["win_rate"] >= 65
            and setup["net_profit"] > 0
        ):
            return (
                "Increase confidence weighting "
                "for this setup."
            )

        return (
            "Maintain current rules until "
            "more data becomes available."
        )


if __name__ == "__main__":

    engine = AdaptiveLearningEngine()

    result = engine.analyze()

    print("\n================================")
    print(" STRATPILOT ADAPTIVE LEARNING")
    print("================================")

    print(f"Status          : {result['status']}")

    if result["status"] == "READY":

        print(f"Trades Learned  : {result['trades']}")
        print(f"Best Setup      : {result['best_setup']}")

        print()

        for setup, stats in result["report"].items():

            print(setup)
            print("------------------------------")
            print(f"Count           : {stats['count']}")
            print(f"Win Rate        : {stats['win_rate']}%")
            print(
                f"Avg Confidence  : "
                f"{stats['average_confidence']}%"
            )
            print(
                f"Net Profit      : "
                f"${stats['net_profit']}"
            )
            print()

        print("Recommendation")
        print("------------------------------")
        print(result["recommendation"])

    else:

        print(result["message"])

    print("\nThink First. Trade Second.")
