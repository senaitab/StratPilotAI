import json
from pathlib import Path


class StrategyIntelligence:
    """
    Stage 26.8
    Analyze historical strategy performance.
    """

    def __init__(self):
        self.history_file = (
            Path(__file__).parent.parent
            / "memory"
            / "trade_history.json"
        )

    def load_history(self):
        if not self.history_file.exists():
            return []

        try:
            with open(self.history_file, "r") as f:
                return json.load(f)
        except Exception:
            return []

    def analyze(self):
        history = self.load_history()

        if not history:
            return {
                "strategies": {},
                "best_strategy": None,
                "worst_strategy": None,
            }

        strategies = {}

        for trade in history:

            name = trade.get("strategy", "UNKNOWN")

            if name not in strategies:
                strategies[name] = {
                    "trades": 0,
                    "wins": 0,
                    "losses": 0,
                    "confidence_sum": 0.0,
                    "profit_sum": 0.0,
                }

            s = strategies[name]

            s["trades"] += 1
            s["confidence_sum"] += float(
                trade.get("confidence", 0)
            )
            s["profit_sum"] += float(
                trade.get("profit_loss", 0)
            )

            if trade.get("result") == "WIN":
                s["wins"] += 1
            else:
                s["losses"] += 1

        best = None
        worst = None

        for name, s in strategies.items():

            trades = s["trades"]

            s["win_rate"] = round(
                (s["wins"] / trades) * 100,
                2,
            )

            s["avg_confidence"] = round(
                s["confidence_sum"] / trades,
                2,
            )

            s["avg_profit"] = round(
                s["profit_sum"] / trades,
                2,
            )

            if best is None or s["win_rate"] > strategies[best]["win_rate"]:
                best = name

            if worst is None or s["win_rate"] < strategies[worst]["win_rate"]:
                worst = name

        return {
            "strategies": strategies,
            "best_strategy": best,
            "worst_strategy": worst,
        }


if __name__ == "__main__":

    ai = StrategyIntelligence()

    report = ai.analyze()

    print("\n====================================")
    print(" STRATPILOT STRATEGY INTELLIGENCE ")
    print("====================================")

    print(
        f"\nStrategies Analyzed : {len(report['strategies'])}"
    )

    if report["best_strategy"]:

        best = report["strategies"][report["best_strategy"]]

        print("\nBest Strategy")
        print("----------------------------")
        print(report["best_strategy"])
        print(f"Trades        : {best['trades']}")
        print(f"Win Rate      : {best['win_rate']}%")
        print(f"Avg Confidence: {best['avg_confidence']}%")
        print(f"Avg Profit    : ${best['avg_profit']}")

    if report["worst_strategy"]:

        worst = report["strategies"][report["worst_strategy"]]

        print("\nWorst Strategy")
        print("----------------------------")
        print(report["worst_strategy"])
        print(f"Win Rate      : {worst['win_rate']}%")

    print("\nThink First. Trade Second.")
