from typing import Any, Dict

from intelligence.strategy_intelligence import StrategyIntelligence


class SetupAdvisor:
    """
    Stage 26.9
    Uses historical strategy performance to produce
    an advisory confidence adjustment.
    """

    def __init__(self) -> None:
        self.intelligence = StrategyIntelligence()

    def evaluate(self, strategy_name: str) -> Dict[str, Any]:
        report = self.intelligence.analyze()
        strategies = report.get("strategies", {})

        if strategy_name not in strategies:
            return {
                "status": "NEW SETUP",
                "strategy": strategy_name,
                "trades": 0,
                "win_rate": 0.0,
                "average_profit": 0.0,
                "confidence_adjustment": 0,
                "recommendation": (
                    "No historical data. Keep normal risk and collect results."
                ),
            }

        strategy = strategies[strategy_name]

        trades = int(strategy.get("trades", 0))
        win_rate = float(strategy.get("win_rate", 0.0))
        average_profit = float(strategy.get("avg_profit", 0.0))

        if trades < 5:
            status = "LEARNING"
            adjustment = 0
            recommendation = (
                "Not enough history to change confidence."
            )

        elif win_rate >= 70 and average_profit > 0:
            status = "FAVOR"
            adjustment = 3
            recommendation = (
                "Historical performance supports a small confidence increase."
            )

        elif win_rate >= 55 and average_profit >= 0:
            status = "NEUTRAL"
            adjustment = 0
            recommendation = (
                "Historical performance is acceptable. Keep current weighting."
            )

        else:
            status = "CAUTION"
            adjustment = -3
            recommendation = (
                "Historical performance is weak. Reduce confidence and risk."
            )

        return {
            "status": status,
            "strategy": strategy_name,
            "trades": trades,
            "win_rate": win_rate,
            "average_profit": average_profit,
            "confidence_adjustment": adjustment,
            "recommendation": recommendation,
        }


if __name__ == "__main__":
    advisor = SetupAdvisor()

    result = advisor.evaluate("SPY-CALL-A")

    print("\n====================================")
    print(" STRATPILOT HISTORICAL SETUP ADVISOR")
    print("====================================")

    print(f"Status                : {result['status']}")
    print(f"Strategy              : {result['strategy']}")
    print(f"Historical Trades     : {result['trades']}")
    print(f"Win Rate              : {result['win_rate']}%")
    print(f"Average Profit        : ${result['average_profit']}")
    print(
        f"Confidence Adjustment : "
        f"{result['confidence_adjustment']}"
    )

    print("\nRecommendation")
    print("------------------------------------")
    print(result["recommendation"])

    print("\nThink First. Trade Second.")
