import json
from pathlib import Path


class MetricsEngine:

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

    def calculate(self):
        trades = self.load_history()

        total = len(trades)

        if total == 0:
            return {
                "total_trades": 0,
                "wins": 0,
                "losses": 0,
                "win_rate": 0.0,
                "average_confidence": 0.0,
                "gross_profit": 0.0,
                "gross_loss": 0.0,
                "net_profit": 0.0,
                "profit_factor": 0.0,
                "expectancy": 0.0,
                "largest_win": 0.0,
                "largest_loss": 0.0,
                "health_score": 0.0,
                "performance": "NO DATA",
                "recommendation": "Record trades before evaluating performance.",
            }

        pnl_values = []

        for trade in trades:
            pnl = trade.get("realized_pnl", trade.get("pnl", 0))
            pnl_values.append(float(pnl))

        wins = [p for p in pnl_values if p > 0]
        losses = [p for p in pnl_values if p < 0]

        gross_profit = sum(wins)
        gross_loss = abs(sum(losses))
        net_profit = sum(pnl_values)

        win_count = len(wins)
        loss_count = len(losses)

        win_rate = round((win_count / total) * 100, 2)

        avg_confidence = round(
            sum(trade.get("confidence", 0) for trade in trades) / total,
            2,
        )

        avg_win = round(gross_profit / win_count, 2) if win_count else 0.0
        avg_loss = round(gross_loss / loss_count, 2) if loss_count else 0.0

        profit_factor = (
            round(gross_profit / gross_loss, 2)
            if gross_loss > 0
            else 0.0
        )

        expectancy = round(
            ((win_rate / 100) * avg_win) -
            ((1 - (win_rate / 100)) * avg_loss),
            2,
        )

        largest_win = max(pnl_values) if pnl_values else 0.0
        largest_loss = min(pnl_values) if pnl_values else 0.0

        health_score = self.health_score(
            win_rate,
            profit_factor,
            avg_confidence,
            net_profit,
        )

        performance = self.performance_label(health_score)

        recommendation = self.recommendation(performance)

        return {
            "total_trades": total,
            "wins": win_count,
            "losses": loss_count,
            "win_rate": win_rate,
            "average_confidence": avg_confidence,
            "gross_profit": round(gross_profit, 2),
            "gross_loss": round(gross_loss, 2),
            "net_profit": round(net_profit, 2),
            "average_win": avg_win,
            "average_loss": avg_loss,
            "profit_factor": profit_factor,
            "expectancy": expectancy,
            "largest_win": round(largest_win, 2),
            "largest_loss": round(largest_loss, 2),
            "health_score": health_score,
            "performance": performance,
            "recommendation": recommendation,
        }

    def health_score(self, win_rate, profit_factor, confidence, net_profit):
        score = 0

        score += min(win_rate, 100) * 0.35
        score += min(profit_factor * 20, 100) * 0.25
        score += min(confidence, 100) * 0.25

        if net_profit > 0:
            score += 15

        return round(min(score, 100), 2)

    def performance_label(self, score):
        if score >= 95:
            return "ELITE"
        if score >= 85:
            return "EXCELLENT"
        if score >= 70:
            return "GOOD"
        if score >= 50:
            return "FAIR"
        return "WEAK"

    def recommendation(self, performance):
        if performance in ["ELITE", "EXCELLENT"]:
            return "KEEP CURRENT STRATEGY"
        if performance == "GOOD":
            return "CONTINUE WITH NORMAL RISK"
        if performance == "FAIR":
            return "REDUCE RISK AND REVIEW SETUPS"
        return "PAUSE AND REVIEW PERFORMANCE"


if __name__ == "__main__":

    engine = MetricsEngine()
    report = engine.calculate()

    print("\n================================")
    print(" STRATPILOT METRICS AI")
    print("================================")

    print(f"Health Score       : {report['health_score']}")
    print(f"Performance        : {report['performance']}")
    print()
    print(f"Total Trades       : {report['total_trades']}")
    print(f"Wins               : {report['wins']}")
    print(f"Losses             : {report['losses']}")
    print(f"Win Rate           : {report['win_rate']}%")
    print(f"Average Confidence : {report['average_confidence']}%")
    print()
    print(f"Gross Profit       : ${report['gross_profit']}")
    print(f"Gross Loss         : ${report['gross_loss']}")
    print(f"Net Profit         : ${report['net_profit']}")
    print(f"Profit Factor      : {report['profit_factor']}")
    print(f"Expectancy         : ${report['expectancy']}")
    print()
    print(f"Average Win        : ${report.get('average_win', 0)}")
    print(f"Average Loss       : ${report.get('average_loss', 0)}")
    print(f"Largest Win        : ${report['largest_win']}")
    print(f"Largest Loss       : ${report['largest_loss']}")
    print()
    print("Recommendation")
    print("------------------------------")
    print(report["recommendation"])

    print("\nThink First. Trade Second.")
