import json
from pathlib import Path


class StatisticsEngine:

    def __init__(self):
        self.history_file = Path("trade_history.json")

    def calculate(self):

        if not self.history_file.exists():
            return {
                "total_trades": 0,
                "wins": 0,
                "losses": 0,
                "win_rate": 0.0,
                "average_confidence": 0.0,
                "buy_trades": 0,
                "wait_trades": 0,
            }

        with open(self.history_file, "r") as f:
            trades = json.load(f)

        total = len(trades)

        buy_trades = sum(
            1 for trade in trades
            if trade.get("decision") == "BUY"
        )

        wait_trades = sum(
            1 for trade in trades
            if trade.get("decision") == "WAIT"
        )

        confidence = sum(
            trade.get("confidence", 0)
            for trade in trades
        )

        average_confidence = (
            confidence / total if total else 0
        )

        # Placeholder until completed trades exist
        wins = 0
        losses = 0
        win_rate = 0.0

        return {

            "total_trades": total,

            "wins": wins,

            "losses": losses,

            "win_rate": round(win_rate, 2),

            "average_confidence": round(
                average_confidence,
                2
            ),

            "buy_trades": buy_trades,

            "wait_trades": wait_trades,
        }


if __name__ == "__main__":

    stats = StatisticsEngine()

    report = stats.calculate()

    print("\n==============================")
    print(" STRATPILOT STATISTICS")
    print("==============================")

    for key, value in report.items():
        print(f"{key:<22}: {value}")

    print("\nThink First. Trade Second.")
