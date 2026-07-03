from planner.trade_planner import TradePlanner
from portfolio.portfolio_adapter import PortfolioAdapter


class PositionSizer:

    def __init__(self):
        self.planner = TradePlanner()
        self.portfolio = PortfolioAdapter()

    def calculate(self):
        plan = self.planner.build_plan()
        account = self.portfolio.snapshot()

        equity = account["equity"]
        risk_pct = 1.0

        risk_budget = equity * (risk_pct / 100)

        option_price = plan["contract"]["ask"]
        contract_cost = option_price * 100

        underlying_risk = plan["risk"]
        risk_per_contract = underlying_risk * 100

        contracts = int(risk_budget // risk_per_contract)

        if plan["decision"] != "BUY":
            contracts = 0

        if plan["confidence"] < 85:
            contracts = max(0, contracts - 1)

        capital_required = contracts * contract_cost
        total_risk = contracts * risk_per_contract

        if contracts <= 0:
            status = "REJECTED"
            reason = "No contracts allowed under risk rules."
        elif capital_required > account["buying_power"]:
            status = "REJECTED"
            reason = "Not enough buying power."
        else:
            status = "APPROVED"
            reason = "Position size approved."

        return {
            "decision": plan["decision"],
            "status": status,
            "reason": reason,
            "contracts": contracts,
            "equity": equity,
            "risk_pct": risk_pct,
            "risk_budget": round(risk_budget, 2),
            "risk_per_contract": round(risk_per_contract, 2),
            "total_risk": round(total_risk, 2),
            "contract_cost": round(contract_cost, 2),
            "capital_required": round(capital_required, 2),
            "confidence": plan["confidence"],
            "trade_grade": plan["grade"],
            "plan": plan,
        }


if __name__ == "__main__":

    sizer = PositionSizer()
    result = sizer.calculate()

    print("\n==============================")
    print(" STRATPILOT POSITION SIZER")
    print("==============================")

    print(f"Decision         : {result['decision']}")
    print(f"Status           : {result['status']}")
    print(f"Reason           : {result['reason']}")
    print(f"Contracts        : {result['contracts']}")
    print(f"Equity           : {result['equity']}")
    print(f"Risk %           : {result['risk_pct']}")
    print(f"Risk Budget      : {result['risk_budget']}")
    print(f"Risk/Contract    : {result['risk_per_contract']}")
    print(f"Total Risk       : {result['total_risk']}")
    print(f"Contract Cost    : {result['contract_cost']}")
    print(f"Capital Required : {result['capital_required']}")
    print(f"Confidence       : {result['confidence']}")
    print(f"Trade Grade      : {result['trade_grade']}")

    print("\nThink First. Trade Second.")
