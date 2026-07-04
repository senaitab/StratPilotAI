from planner.trade_planner import TradePlanner
from sizing.position_sizer import PositionSizer
from risk.risk_manager import RiskManager
from execution.execution_guard import ExecutionGuard


class ExecutionSimulator:

    COMMISSION = 0.65
    SLIPPAGE = 0.02

    def __init__(self):
        self.planner = TradePlanner()
        self.sizer = PositionSizer()
        self.risk = RiskManager()
        self.guard = ExecutionGuard()

    def simulate(self):

        plan = self.planner.build_plan()
        sizing = self.sizer.calculate()
        risk = self.risk.evaluate()
        guard = self.guard.evaluate()

        if guard["status"] != "APPROVED":
            return {
                "status": "BLOCKED",
                "reason": "Execution Guard denied trade."
            }

        contract = plan["contract"]

        entry_price = contract["ask"]

        fill_price = round(
            entry_price + self.SLIPPAGE,
            2
        )

        current_price = round(
            fill_price + 0.23,
            2
        )

        pnl = round(
            (current_price - fill_price)
            * 100
            * sizing["contracts"],
            2
        )

        capital = round(
            fill_price
            * 100
            * sizing["contracts"],
            2
        )

        return {

            "status": "SIMULATION COMPLETE",

            "decision": plan["decision"],

            "symbol": plan["symbol"],

            "contract": contract,

            "contracts": sizing["contracts"],

            "entry_price": fill_price,

            "current_price": current_price,

            "capital": capital,

            "commission": self.COMMISSION,

            "slippage": self.SLIPPAGE,

            "pnl": pnl,

            "stop_loss": plan["stop_loss"],

            "target_1": plan["target_1"],

            "target_2": plan["target_2"],

            "risk_status": risk["status"],

            "execution": guard["execution"]
        }


if __name__ == "__main__":

    simulator = ExecutionSimulator()

    report = simulator.simulate()

    print("\n==============================")
    print(" STRATPILOT EXECUTION SIMULATOR")
    print("==============================")

    if report["status"] == "BLOCKED":

        print(report["reason"])

    else:

        c = report["contract"]

        print(f"Decision      : {report['decision']}")
        print(f"Status        : {report['status']}")
        print()

        print("Contract")
        print("------------------------------")
        print(
            f"{c['symbol']} "
            f"{c['strike']} "
            f"{c['type']} "
            f"{c['expiration']}"
        )

        print()
        print(f"Contracts     : {report['contracts']}")
        print(f"Entry Price   : {report['entry_price']}")
        print(f"Current Price : {report['current_price']}")
        print(f"Capital Used  : ${report['capital']}")
        print(f"Commission    : ${report['commission']}")
        print(f"Slippage      : ${report['slippage']}")
        print(f"Unrealized P/L: ${report['pnl']}")
        print(f"Stop Loss     : {report['stop_loss']}")
        print(f"Target 1      : {report['target_1']}")
        print(f"Target 2      : {report['target_2']}")
        print(f"Risk Status   : {report['risk_status']}")
        print(f"Execution     : {report['execution']}")

    print("\nThink First. Trade Second.")
