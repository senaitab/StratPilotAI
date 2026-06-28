from datetime import datetime
import json
import os


class TradeJournalAI:

    def __init__(self):
        self.log_dir = "logs"
        self.log_file = os.path.join(self.log_dir, "trade_journal.json")

        os.makedirs(self.log_dir, exist_ok=True)

        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                json.dump([], f)

    def record(self,
               market,
               risk,
               strategy,
               options,
               position,
               commander,
               execution):

        entry = {
            "timestamp": datetime.now().isoformat(),

            "market": market,
            "risk": risk,
            "strategy": strategy,
            "options": options,
            "position": position,
            "commander": commander,
            "execution": execution
        }

        with open(self.log_file, "r") as f:
            data = json.load(f)

        data.append(entry)

        with open(self.log_file, "w") as f:
            json.dump(data, f, indent=4)

        return entry


if __name__ == "__main__":

    journal = TradeJournalAI()

    sample = journal.record(
        market={"bias": "NEUTRAL"},
        risk={"decision": "NO TRADE"},
        strategy={"recommendation": "WAIT"},
        options={"decision": "WAIT"},
        position={"contracts": 0},
        commander={"decision": "TRADE REJECTED"},
        execution={"status": "NOT READY"}
    )

    print("================================")
    print("   STRATPILOT TRADE JOURNAL")
    print("================================")
    print("Trade recorded successfully.")
    print(sample["timestamp"])
