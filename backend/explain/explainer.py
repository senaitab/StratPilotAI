from decision.decision_engine import DecisionEngine


class ExplainableAI:

    def __init__(self):
        self.engine = DecisionEngine()

    def explain(self):
        decision = self.engine.decide()

        market = decision["market"]
        commander = decision["commander"]
        best_contract = decision["best_contract"]
        contract = best_contract["contract"]

        reasons = []

        if market["market_status"] == "OPEN":
            reasons.append("✓ Market is open.")

        if commander["regime"] in ["NORMAL", "RANGE", "BULL"]:
            reasons.append(f"✓ Market regime is tradable: {commander['regime']}.")

        if commander["consensus"]["decision"] == "BUY":
            reasons.append("✓ Consensus engine recommends BUY.")

        if commander["confidence"]["confidence"] >= 85:
            reasons.append(
                f"✓ Confidence is high: {commander['confidence']['confidence']:.2f}%."
            )

        if commander["execution"]["status"] == "EXECUTE":
            reasons.append("✓ Execution AI approved.")

        if best_contract["rating"] == "APPROVED":
            reasons.append("✓ Best option contract is approved.")

        if not decision["reasons"]:
            reasons.append("✓ No blocking conditions found.")

        return {
            "decision": decision,
            "reasons": reasons,
            "contract": contract,
        }


if __name__ == "__main__":

    ai = ExplainableAI()
    result = ai.explain()

    d = result["decision"]
    commander = d["commander"]
    contract = result["contract"]

    print("\n==============================")
    print(" STRATPILOT EXPLAINABLE AI")
    print("==============================")

    print(f"Decision    : {d['final_decision']}")
    print(f"Confidence  : {commander['confidence']['confidence']:.2f}")
    print(f"Level       : {commander['confidence']['level']}")
    print(f"Trade Grade : {commander['consensus']['grade']}")

    print("\nContract")
    print("------------------------------")
    print(f"{contract['symbol']} {contract['strike']} {contract['type']} {contract['expiration']}")

    print("\nWhy?")
    print("------------------------------")
    for reason in result["reasons"]:
        print(reason)

    print("\nThink First. Trade Second.")
