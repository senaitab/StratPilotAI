import json
from pathlib import Path
from datetime import datetime


class TradeMemory:
    """
    Stage 26.7
    Persistent storage for completed trades.
    """

    def __init__(self):
        self.file = Path(__file__).parent / "trade_history.json"

        if not self.file.exists():
            self.file.write_text("[]")

    def load(self):
        try:
            with open(self.file, "r") as f:
                return json.load(f)
        except Exception:
            return []

    def save(self, trades):
        with open(self.file, "w") as f:
            json.dump(trades, f, indent=4)

    def record_trade(self, trade):

        history = self.load()

        trade["recorded_at"] = datetime.now().isoformat()

        history.append(trade)

        self.save(history)

        return trade

    def statistics(self):

        history = self.load()

        total = len(history)

        wins = sum(1 for t in history if t.get("result") == "WIN")

        losses = sum(1 for t in history if t.get("result") == "LOSS")

        win_rate = 0

        if total > 0:
            win_rate = round((wins / total) * 100, 2)

        return {
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate
        }


if __name__ == "__main__":

    memory = TradeMemory()

    sample_trade = {
        "symbol": "SPY",
        "strategy": "SPY-CALL-A",
        "decision": "BUY",
        "confidence": 91.4,
        "profit_loss": 152.35,
        "result": "WIN"
    }

    memory.record_trade(sample_trade)

    stats = memory.statistics()

    print("\n==============================")
    print(" STRATPILOT TRADE MEMORY ")
    print("==============================")

    print(f"Total Trades : {stats['total_trades']}")
    print(f"Wins         : {stats['wins']}")
    print(f"Losses       : {stats['losses']}")
    print(f"Win Rate     : {stats['win_rate']}%")

    print("\nThink First. Trade Second.")
