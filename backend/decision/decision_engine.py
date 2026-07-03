from market.market_adapter import MarketAdapter
from options.contract_scanner import ContractScanner
from commander.commander_ai import CommanderAI


class DecisionEngine:

    def __init__(self):
        self.market = MarketAdapter()
        self.contract_scanner = ContractScanner()
        self.commander = CommanderAI()

    def decide(self):
        market = self.market.snapshot()
        contracts = self.contract_scanner.scan()

        sample_report = {
            "market": {
                "change_pct": market["change_pct"],
                "recommendation": "BUY",
            },
            "risk": {
                "status": "SAFE",
            },
            "strategy": {
                "confidence": 0.82,
            },
            "options": {
                "decision": "BUY",
            },
            "position": {
                "decision": "ALLOW",
                "status": "APPROVED",
            },
            "portfolio": {
                "status": "HEALTHY",
            },
        }

        commander_report = self.commander.command(sample_report)

        best_contract = contracts["recommended"]

        reasons = []

        if market["market_status"] == "CLOSED":
            reasons.append("Market is closed.")

        if commander_report["confidence"]["confidence"] < 85:
            reasons.append("Confidence below 85%.")

        if commander_report["execution"]["status"] != "EXECUTE":
            reasons.append("ExecutionAI did not approve.")

        if best_contract["rating"] != "APPROVED":
            reasons.append("Best contract not approved.")

        if reasons:
            final_decision = "WAIT"
        else:
            final_decision = "BUY"

        return {
            "final_decision": final_decision,
            "market": market,
            "commander": commander_report,
            "best_contract": best_contract,
            "reasons": reasons,
        }


if __name__ == "__main__":
    engine = DecisionEngine()
    report = engine.decide()

    contract = report["best_contract"]["contract"]

    print("\n==============================")
    print(" STRATPILOT DECISION ENGINE")
    print("==============================")

    print(f"Final Decision : {report['final_decision']}")
    print(f"Market Status  : {report['market']['market_status']}")
    print(f"Regime         : {report['commander']['regime']}")
    print(f"Consensus      : {report['commander']['consensus']['decision']}")
    print(f"Score          : {report['commander']['consensus']['score']}")
    print(f"Confidence     : {report['commander']['confidence']['confidence']}")
    print(f"Level          : {report['commander']['confidence']['level']}")
    print(f"Execution      : {report['commander']['execution']['status']}")

    print("\nBest Contract")
    print("------------------------------")
    print(f"{contract['symbol']} {contract['strike']} {contract['type']} {contract['expiration']}")
    print(f"Contract Score : {report['best_contract']['score']}")
    print(f"Rating         : {report['best_contract']['rating']}")

    print("\nReasons")
    print("------------------------------")
    if report["reasons"]:
        for reason in report["reasons"]:
            print("-", reason)
    else:
        print("- All decision checks passed.")

    print("\nThink First. Trade Second.")
