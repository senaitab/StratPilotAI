from intelligence.market_ai import MarketAI
from strategy.strategy_ai import StrategyAI


class OptionsAI:

    def __init__(self):
        self.market = MarketAI()
        self.strategy = StrategyAI()

    def analyze(self):

        market = self.market.analyze()
        strategy = self.strategy.analyze()

        spy = market["price"]
        bias = market["bias"]
        recommendation = strategy["recommendation"]

        if recommendation == "CALL":
            contracts = [
                round(spy + 1),
                round(spy + 2),
                round(spy + 3),
                round(spy + 4),
            ]
            option_type = "CALL"

        elif recommendation == "PUT":
            contracts = [
                round(spy - 1),
                round(spy - 2),
                round(spy - 3),
                round(spy - 4),
            ]
            option_type = "PUT"

        else:
            return {
                "decision": "WAIT",
                "reason": "StrategyAI did not approve a trade."
            }

        best_contract = contracts[1]

        return {
            "decision": "READY",
            "spy": spy,
            "bias": bias,
            "type": option_type,
            "contract": best_contract,
            "confidence": strategy["confidence"]
        }


if __name__ == "__main__":

    ai = OptionsAI()

    report = ai.analyze()

    print()
    print("================================")
    print("      STRATPILOT OPTIONS AI")
    print("================================")

    for key, value in report.items():
        print(f"{key:<12}: {value}")
