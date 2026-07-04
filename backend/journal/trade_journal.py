import json
from pathlib import Path
from datetime import datetime

from decision.decision_engine import DecisionEngine


class TradeJournal:

    def __init__(self):
        self.engine = DecisionEngine()
        self.file = Path("trade_history.json")

    def record_trade(self):

        report = self.engine.decide()

        contract = report["best_contract"]["contract"]

        trade = {
            "timestamp": datetime.now().isoformat(),
            "symbol": contract["symbol"],
            "expiration": contract["expiration"],
            "strike": contract["strike"],
            "type": contract["type"],
            "entry_price": contract["ask"],
            "contracts": 1,
            "confidence": report["commander"]["confidence"]["confidence"],
            "trade_grade": report["commander"]["consensus"]["grade"],
            "decision": report["final_decision"],
            "status": "OPEN"
        }

        history = []

        if self.file.exists():
            try:
                with open(self.file, "r") as f:
                    history = json.load(f)
            except Exception:
                history = []

        history.append(trade)

        with open(self.file, "w") as f:
            json.dump(history, f, indent=4)

        return trade


if __name__ == "__main__":

    journal = TradeJournal()

    trade = journal.record_trade()

    print()
    print("==============================")
    print(" STRATPILOT TRADE JOURNAL")
    print("==============================")

    for key, value in trade.items():
        print(f"{key:15}: {value}")

    print()
    print("Trade saved successfully.")
    print()
    print("Think First. Trade Second.")
