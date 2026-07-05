import json
from pathlib import Path

from portfolio.exposure import ExposureEngine
from portfolio.allocation import AllocationEngine


class PortfolioManager:

    def __init__(self):
        self.file = Path("portfolio/portfolio.json")
        self.exposure = ExposureEngine()
        self.allocation = AllocationEngine()

    def load_portfolio(self):
        with open(self.file, "r") as f:
            return json.load(f)

    def analyze(self):
        portfolio = self.load_portfolio()
        exposure = self.exposure.calculate()
        allocation = self.allocation.evaluate(portfolio)

        if (
            portfolio["portfolio_health"] == "EXCELLENT"
            and exposure["risk"] == "LOW"
            and allocation["approved"]
        ):
            verdict = "Portfolio is healthy. Capital allocation is within limits. Risk exposure is LOW."
            status = "APPROVED"
        else:
            verdict = "Portfolio conditions require caution."
            status = "CAUTION"

        return {
            "portfolio": portfolio,
            "exposure": exposure,
            "allocation": allocation,
            "status": status,
            "verdict": verdict,
        }


if __name__ == "__main__":

    manager = PortfolioManager()
    report = manager.analyze()

    p = report["portfolio"]
    e = report["exposure"]
    a = report["allocation"]

    print("\n==============================")
    print(" STRATPILOT PORTFOLIO AI")
    print("==============================")

    print(f"Portfolio Health : {p['portfolio_health']}")
    print(f"Cash Available   : ${p['cash']}")
    print(f"Buying Power     : ${p['buying_power']}")
    print(f"Capital Used     : ${p['capital_used']}")
    print(f"Open Positions   : {p['open_positions']}")
    print(f"Daily P/L        : ${p['daily_pl']}")

    print("\nExposure")
    print("------------------------------")
    print(f"Delta            : {e['delta']}")
    print(f"Theta            : {e['theta']}")
    print(f"Gamma            : {e['gamma']}")
    print(f"Vega             : {e['vega']}")
    print(f"Risk             : {e['risk']}")

    print("\nAllocation")
    print("------------------------------")
    print(f"Status           : {a['status']}")
    print(f"Recommendation   : {a['recommendation']}")
    print(f"Max Position     : {a['max_position_size']} Contract")
    print(f"Capital Remaining: ${a['capital_remaining']}")
    print(f"Capital Usage %  : {a['capital_usage_pct']}%")

    print("\nPortfolio Verdict")
    print("------------------------------")
    print(report["verdict"])

    print("\nThink First. Trade Second.")
