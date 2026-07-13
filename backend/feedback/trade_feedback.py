from datetime import datetime


class TradeFeedback:

    def process(self, trade):

        pnl = float(trade.get("profit_loss", 0))

        if pnl > 0:
            result = "WIN"
        elif pnl < 0:
            result = "LOSS"
        else:
            result = "BREAKEVEN"

        report = {

            "timestamp": datetime.now().isoformat(),

            "symbol": trade.get("symbol", "UNKNOWN"),

            "strategy": trade.get("strategy", "UNKNOWN"),

            "decision": trade.get("decision", "UNKNOWN"),

            "confidence": trade.get("confidence", 0),

            "profit_loss": pnl,

            "result": result,

        }

        return report


if __name__ == "__main__":

    feedback = TradeFeedback()

    sample_trade = {

        "symbol": "SPY",

        "strategy": "SPY-CALL-A",

        "decision": "BUY",

        "confidence": 91.4,

        "profit_loss": 152.35,

    }

    report = feedback.process(sample_trade)

    print("\n===================================")
    print(" STRATPILOT TRADE FEEDBACK")
    print("===================================")

    for key, value in report.items():
        print(f"{key:<14}: {value}")

    print("\nThink First. Trade Second.")
