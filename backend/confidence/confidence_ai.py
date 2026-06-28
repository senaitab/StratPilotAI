from intelligence.market_ai import MarketAI
from risk.risk_ai import RiskAI
from strategy.strategy_ai import StrategyAI
from options.options_ai import OptionsAI
from position.position_ai import PositionAI
from execution.execution_ai import ExecutionAI


class ConfidenceAI:
    def __init__(self):
        self.market_ai = MarketAI()
        self.risk_ai = RiskAI()
        self.strategy_ai = StrategyAI()
        self.options_ai = OptionsAI()
        self.position_ai = PositionAI()
        self.execution_ai = ExecutionAI()

    def analyze(self):
        market = self.market_ai.analyze()
        risk = self.risk_ai.analyze()
        strategy = self.strategy_ai.analyze()
        options = self.options_ai.analyze()
        position = self.position_ai.analyze()
        execution = self.execution_ai.execute()

        score = 0
        reasons = []

        if market["session"] != "CLOSED":
            score += 15
            reasons.append("Market session is active.")
        else:
            reasons.append("Market is closed.")

        if market["bias"] != "NEUTRAL":
            score += 15
            reasons.append(f"Market bias detected: {market['bias']}.")
        else:
            reasons.append("Market bias is neutral.")

        if risk["status"] == "APPROVED":
            score += 20
            reasons.append("RiskAI approved risk.")
        else:
            reasons.append("RiskAI rejected risk.")

        if strategy["recommendation"] != "WAIT":
            score += 20
            reasons.append(f"StrategyAI recommends {strategy['recommendation']}.")
        else:
            reasons.append("StrategyAI says WAIT.")

        if options["decision"] == "READY":
            score += 15
            reasons.append("OptionsAI selected a contract.")
        else:
            reasons.append("OptionsAI is waiting.")

        if position["decision"] == "APPROVED":
            score += 10
            reasons.append("PositionAI approved sizing.")
        else:
            reasons.append("PositionAI rejected sizing.")

        if execution["status"] == "READY":
            score += 5
            reasons.append("ExecutionAI is ready.")
        else:
            reasons.append("ExecutionAI is not ready.")

        if score >= 85:
            rating = "HIGH CONFIDENCE"
        elif score >= 65:
            rating = "MODERATE CONFIDENCE"
        elif score >= 40:
            rating = "LOW CONFIDENCE"
        else:
            rating = "NO TRADE CONFIDENCE"

        return {
            "score": score,
            "rating": rating,
            "market": market,
            "risk": risk,
            "strategy": strategy,
            "options": options,
            "position": position,
            "execution": execution,
            "reasons": reasons,
        }


if __name__ == "__main__":
    ai = ConfidenceAI()
    report = ai.analyze()

    print("\n===================================")
    print("      STRATPILOT CONFIDENCE AI")
    print("===================================")
    print(f"Score  : {report['score']}%")
    print(f"Rating : {report['rating']}")
    print("-----------------------------------")
    print("Reasons:")
    for reason in report["reasons"]:
        print(f"- {reason}")
    print("===================================")
    print("Think First. Trade Second.")
