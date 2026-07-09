import json
from pathlib import Path


class StrategyAnalyzer:

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
                "message": "No trade history found.",
                "setups": {},
                "recommendation": "Record trades before analyzing strategy.",
            }

        setups = {}

        for trade in trades:
            grade = trade.get("trade_grade", "UNKNOWN")
            decision = trade.get("decision", "UNKNOWN")
            symbol = trade.get("symbol", "UNKNOWN")
            option_type = trade.get("type", "UNKNOWN")

            setup_key = f"{symbol}-{option_type}-{grade}-{decision}"

            if setup_key not in setups:
                setups[setup_key] = {
                    "count": 0,
                    "total_confidence": 0,
                    "wins": 0,
                    "losses": 0,
                    "net_pnl": 0.0,
                }

            pnl = float(trade.get("realized_pnl", trade.get("pnl", 0)))

            setups[setup_key]["count"] += 1
            setups[setup_key]["total_confidence"] += trade.get("confidence", 0)
            setups[setup_key]["net_pnl"] += pnl

            if pnl > 0:
                setups[setup_key]["wins"] += 1
            elif pnl < 0:
                setups[setup_key]["losses"] += 1

        ranked = {}

        for key, data in setups.items():
            count = data["count"]
            wins = data["wins"]
            losses = data["losses"]

            win_rate = round((wins / count) * 100, 2) if count else 0.0
            avg_confidence = round(data["total_confidence"] / count, 2)

            ranked[key] = {
                "count": count,
                "wins": wins,
                "losses": losses,
                "win_rate": win_rate,
                "average_confidence": avg_confidence,
                "net_pnl": round(data["net_pnl"], 2),
            }

        best_setup = max(
            ranked,
            key=lambda k: (
                ranked[k]["net_pnl"],
                ranked[k]["win_rate"],
                ranked[k]["average_confidence"],
            ),
        )

        return {
            "status": "COMPLETE",
            "total_setups": len(ranked),
            "setups": ranked,
            "best_setup": best_setup,
            "recommendation": self.recommendation(ranked[best_setup]),
        }

    def recommendation(self, setup):
        if setup["count"] < 5:
            return "LEARNING MODE: collect more completed trades before trusting setup ranking."

        if setup["win_rate"] >= 65 and setup["net_pnl"] > 0:
            return "FAVOR THIS SETUP."

        if setup["win_rate"] < 45 or setup["net_pnl"] < 0:
            return "AVOID OR REDUCE RISK ON THIS SETUP."

        return "CONTINUE MONITORING THIS SETUP."


if __name__ == "__main__":

    analyzer = StrategyAnalyzer()
    report = analyzer.analyze()

    print("\n================================")
    print(" STRATPILOT STRATEGY ANALYZER")
    print("================================")

    print(f"Status       : {report['status']}")

    if report["status"] != "COMPLETE":
        print(report["message"])
    else:
        print(f"Total Setups : {report['total_setups']}")
        print(f"Best Setup   : {report['best_setup']}")

        print("\nSetups")
        print("------------------------------")

        for setup, data in report["setups"].items():
            print(f"{setup}")
            print(f"  Count      : {data['count']}")
            print(f"  Wins       : {data['wins']}")
            print(f"  Losses     : {data['losses']}")
            print(f"  Win Rate   : {data['win_rate']}%")
            print(f"  Avg Conf   : {data['average_confidence']}%")
            print(f"  Net P/L    : ${data['net_pnl']}")
            print()

        print("Recommendation")
        print("------------------------------")
        print(report["recommendation"])

    print("\nThink First. Trade Second.")
