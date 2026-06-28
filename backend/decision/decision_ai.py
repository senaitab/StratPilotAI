from data.data_cache_ai import DataCacheAI
from strategy.strategy_ai import StrategyAI
from options.options_ai import OptionsAI
from position.position_ai import PositionAI
from learning.learning_ai import LearningAI


class DecisionAI:
    def __init__(self):
        self.data_cache = DataCacheAI()
        self.strategy_ai = StrategyAI()
        self.options_ai = OptionsAI()
        self.position_ai = PositionAI()
        self.learning_ai = LearningAI()

    def vote(self):
        cached = self.data_cache.snapshot()
        market = cached["market"]
        risk = cached["risk"]

        strategy = self.strategy_ai.analyze()
        options = self.options_ai.analyze()
        position = self.position_ai.analyze()
        learning = self.learning_ai.learn()

        votes = {"BUY": 0, "SELL": 0, "WAIT": 0}
        reasons = []

        if market["bias"] in ["BULLISH", "STRONG BULLISH"]:
            votes["BUY"] += 1
            reasons.append("MarketAI bullish.")
        elif market["bias"] in ["BEARISH", "STRONG BEARISH"]:
            votes["SELL"] += 1
            reasons.append("MarketAI bearish.")
        else:
            votes["WAIT"] += 1
            reasons.append("MarketAI neutral.")

        if risk["status"] == "APPROVED":
            votes["BUY"] += 1
            reasons.append("RiskAI approved.")
        else:
            votes["WAIT"] += 1
            reasons.append("RiskAI rejected.")

        if strategy["recommendation"] == "CALL":
            votes["BUY"] += 1
            reasons.append("StrategyAI CALL.")
        elif strategy["recommendation"] == "PUT":
            votes["SELL"] += 1
            reasons.append("StrategyAI PUT.")
        else:
            votes["WAIT"] += 1
            reasons.append("StrategyAI WAIT.")

        if options["decision"] == "READY":
            votes["BUY"] += 1
            reasons.append("OptionsAI ready.")
        else:
            votes["WAIT"] += 1
            reasons.append("OptionsAI waiting.")

        if position["decision"] == "APPROVED":
            votes["BUY"] += 1
            reasons.append("PositionAI approved.")
        else:
            votes["WAIT"] += 1
            reasons.append("PositionAI rejected.")

        if learning and learning["total"] >= 10:
            votes["BUY"] += 1
            reasons.append("LearningAI has enough data.")
        else:
            votes["WAIT"] += 1
            reasons.append("LearningAI needs more history.")

        final_decision = "WAIT"
        if votes["BUY"] > votes["SELL"] and votes["BUY"] > votes["WAIT"]:
            final_decision = "BUY"
        elif votes["SELL"] > votes["BUY"] and votes["SELL"] > votes["WAIT"]:
            final_decision = "SELL"

        return {
            "final_decision": final_decision,
            "votes": votes,
            "market": market,
            "risk": risk,
            "strategy": strategy,
            "options": options,
            "position": position,
            "learning": learning,
            "reasons": reasons,
        }


if __name__ == "__main__":
    ai = DecisionAI()
    report = ai.vote()

    print("\n===================================")
    print("      STRATPILOT DECISION AI")
    print("===================================")
    print(f"Final Decision : {report['final_decision']}")
    print("-----------------------------------")
    print(f"BUY Votes      : {report['votes']['BUY']}")
    print(f"SELL Votes     : {report['votes']['SELL']}")
    print(f"WAIT Votes     : {report['votes']['WAIT']}")
    print("-----------------------------------")
    print(f"Market Bias    : {report['market']['bias']}")
    print(f"Risk Status    : {report['risk']['status']}")
    print(f"Strategy       : {report['strategy']['recommendation']}")
    print(f"Options        : {report['options']['decision']}")
    print(f"Position       : {report['position']['decision']}")
    print("-----------------------------------")
    print("Reasons:")
    for reason in report["reasons"]:
        print(f"- {reason}")
    print("===================================")
    print("Think First. Trade Second.")

