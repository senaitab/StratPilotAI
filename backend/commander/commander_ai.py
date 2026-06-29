from data.data_cache_ai import DataCacheAI
from strategy.strategy_ai import StrategyAI
from options.options_ai import OptionsAI
from position.position_ai import PositionAI
from portfolio.portfolio_ai import PortfolioAI
from learning.learning_ai import LearningAI


class CommanderAI:
    def __init__(self):
        self.cache = DataCacheAI()
        self.strategy = StrategyAI()
        self.options = OptionsAI()
        self.position = PositionAI()
        self.portfolio = PortfolioAI()
        self.learning = LearningAI()

    def command(self):
        cached = self.cache.snapshot()

        market = cached["market"]
        risk = cached["risk"]

        return {
            "market": market,
            "risk": risk,
            "strategy": self.strategy.analyze(),
            "options": self.options.analyze(),
            "position": self.position.analyze(),
            "portfolio": self.portfolio.analyze(risk),
            "learning": self.learning.learn(),
        }

    def vote(self, report):
        buy = 0
        sell = 0
        wait = 0

        for value in report.values():
            if not isinstance(value, dict):
                continue

            decision = (
                value.get("decision")
                or value.get("recommendation")
                or value.get("status")
                or ""
            )

            decision = str(decision).upper()

            if "BUY" in decision or "CALL" in decision or "APPROVED" in decision:
                buy += 1
            elif "SELL" in decision or "PUT" in decision:
                sell += 1
            else:
                wait += 1

        return {
            "buy": buy,
            "sell": sell,
            "wait": wait,
        }

    def final_decision(self, votes):
        if votes["buy"] > votes["sell"] and votes["buy"] > votes["wait"]:
            return "BUY"

        if votes["sell"] > votes["buy"] and votes["sell"] > votes["wait"]:
            return "SELL"

        return "WAIT"


if __name__ == "__main__":
    ai = CommanderAI()

    report = ai.command()
    votes = ai.vote(report)
    decision = ai.final_decision(votes)

    print("\n======================================")
    print("      STRATPILOT COMMANDER AI")
    print("======================================")

    print(f"BUY Votes  : {votes['buy']}")
    print(f"SELL Votes : {votes['sell']}")
    print(f"WAIT Votes : {votes['wait']}")

    print("--------------------------------------")
    print("FINAL DECISION")
    print("--------------------------------------")
    print(decision)

    print("======================================")
    print("Think First. Trade Second.")
