from decision.decision_engine import DecisionEngine


class TradePlanner:

    def __init__(self):
        self.engine = DecisionEngine()

    def build_plan(self):
        decision_report = self.engine.decide()

        market = decision_report["market"]
        commander = decision_report["commander"]
        best = decision_report["best_contract"]
        contract = best["contract"]

        entry = market["price"]
        stop_loss = round(entry - 1.65, 2)
        target_1 = round(entry + 1.85, 2)
        target_2 = round(entry + 4.25, 2)

        risk = round(entry - stop_loss, 2)
        reward = round(target_2 - entry, 2)
        rr = round(reward / risk, 2) if risk > 0 else 0

        if decision_report["final_decision"] == "BUY" and commander["execution"]["approved"]:
            status = "READY TO EXECUTE"
        else:
            status = "WAIT"

        if rr >= 2.5 and commander["confidence"]["confidence"] >= 85:
            grade = "A+"
        elif rr >= 2.0:
            grade = "A"
        elif rr >= 1.5:
            grade = "B"
        else:
            grade = "C"

        return {
            "decision": decision_report["final_decision"],
            "symbol": market["symbol"],
            "contract": contract,
            "entry": entry,
            "stop_loss": stop_loss,
            "target_1": target_1,
            "target_2": target_2,
            "risk": risk,
            "reward": reward,
            "risk_reward": rr,
            "confidence": commander["confidence"]["confidence"],
            "level": commander["confidence"]["level"],
            "grade": grade,
            "status": status,
        }


if __name__ == "__main__":

    planner = TradePlanner()
    plan = planner.build_plan()
    c = plan["contract"]

    print("\n==============================")
    print(" STRATPILOT TRADE PLANNER")
    print("==============================")

    print(f"Decision      : {plan['decision']}")
    print(f"Status        : {plan['status']}")
    print(f"Symbol        : {plan['symbol']}")
    print(f"Contract      : {c['strike']} {c['type']} {c['expiration']}")
    print(f"Entry         : {plan['entry']}")
    print(f"Stop Loss     : {plan['stop_loss']}")
    print(f"Target 1      : {plan['target_1']}")
    print(f"Target 2      : {plan['target_2']}")
    print(f"Risk          : {plan['risk']}")
    print(f"Reward        : {plan['reward']}")
    print(f"Risk/Reward   : {plan['risk_reward']}")
    print(f"Confidence    : {plan['confidence']}")
    print(f"Level         : {plan['level']}")
    print(f"Trade Grade   : {plan['grade']}")

    print("\nThink First. Trade Second.")
