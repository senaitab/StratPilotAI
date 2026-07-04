from decision.decision_engine import DecisionEngine


class PositionMonitor:

    def __init__(self):
        self.engine = DecisionEngine()

    def monitor(self):
        report = self.engine.decide()

        contract = report["best_contract"]["contract"]

        entry = contract["ask"]
        current = round(entry * 1.04, 2)      # simulated live price

        contracts = 1
        multiplier = 100

        pnl = round((current - entry) * contracts * multiplier, 2)

        stop_price = round(entry * 0.87, 2)
        target1 = round(entry * 1.10, 2)
        target2 = round(entry * 1.20, 2)

        if pnl > 0:
            health = "EXCELLENT"
            recommendation = "HOLD POSITION"
        elif pnl == 0:
            health = "NEUTRAL"
            recommendation = "WAIT"
        else:
            health = "WARNING"
            recommendation = "EXIT"

        return {
            "status": "OPEN",
            "entry_price": entry,
            "current_price": current,
            "contracts": contracts,
            "pnl": pnl,
            "stop_loss": stop_price,
            "target1": target1,
            "target2": target2,
            "health": health,
            "recommendation": recommendation,
            "contract": contract
        }


if __name__ == "__main__":

    monitor = PositionMonitor()

    report = monitor.monitor()

    print()
    print("==============================")
    print(" STRATPILOT POSITION MONITOR")
    print("==============================")

    print(f"Status          : {report['status']}")
    print(f"Health          : {report['health']}")
    print()

    c = report["contract"]

    print("Contract")
    print("------------------------------")
    print(
        f"{c['symbol']} "
        f"{c['strike']} "
        f"{c['type']} "
        f"{c['expiration']}"
    )

    print()
    print(f"Entry Price     : ${report['entry_price']:.2f}")
    print(f"Current Price   : ${report['current_price']:.2f}")
    print(f"P/L             : ${report['pnl']:.2f}")
    print()

    print(f"Stop Loss       : ${report['stop_loss']:.2f}")
    print(f"Target 1        : ${report['target1']:.2f}")
    print(f"Target 2        : ${report['target2']:.2f}")
    print()

    print("Recommendation")
    print("------------------------------")
    print(report["recommendation"])

    print()
    print("Think First. Trade Second.")
