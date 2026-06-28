from intelligence.market_ai import MarketAI
from risk.risk_ai import RiskAI
from strategy.strategy_ai import StrategyAI
from options.options_ai import OptionsAI


class CommanderAI:
    def __init__(self):
        self.market_ai = MarketAI()
        self.risk_ai = RiskAI()
        self.strategy_ai = StrategyAI()
        self.options_ai = OptionsAI()

    def decide(self):
        market = self.market_ai.analyze()
        risk = self.risk_ai.analyze()
        strategy = self.strategy_ai.analyze()
        options = self.options_ai.analyze()

        reasons = []

        if market["session"] == "CLOSED":
            reasons.append("Market is closed.")

        if risk["status"] != "APPROVED":
            reasons.append(risk["reason"])

        if strategy["recommendation"] == "WAIT":
            reasons.append("StrategyAI says WAIT.")

        if strategy["confidence"] < 70:
            reasons.append("Strategy confidence below 70%.")

        if options["decision"] != "READY":
            reasons.append(options["reason"])

        if len(reasons) == 0:
            decision = "TRADE APPROVED"
        else:
            decision = "TRADE REJECTED"

        return {
            "decision": decision,
            "market": market,
            "risk": risk,
            "strategy": strategy,
            "options": options,
            "reasons": reasons,
        }


if __name__ == "__main__":
    ai = CommanderAI()
    report = ai.decide()

    print("\n===================================")
    print("      STRATPILOT COMMANDER AI")
    print("===================================")

    print(f"Final Decision : {report['decision']}")
    print("-----------------------------------")
    print(f"Market Session : {report['market']['session']}")
    print(f"Market Bias    : {report['market']['bias']}")
    print(f"Risk Status    : {report['risk']['status']}")
    print(f"Strategy       : {report['strategy']['recommendation']}")
    print(f"Confidence     : {report['strategy']['confidence']}%")
    print("-----------------------------------")

    print("OptionsAI")
    print("-----------------------------------")
    if report["options"]["decision"] == "READY":
        print(f"Contract       : SPY {report['options']['contract']} {report['options']['type']}")
        print(f"Option Score   : {report['options']['confidence']}%")
    else:
        print("Contract       : WAIT")
        print(f"Reason         : {report['options']['reason']}")

    print("-----------------------------------")

    if report["reasons"]:
        print("Reasons:")
        for reason in report["reasons"]:
            print(f"- {reason}")
    else:
        print("Reasons:")
        print("- All systems approved.")

    print("===================================")
    print("Think First. Trade Second.")
