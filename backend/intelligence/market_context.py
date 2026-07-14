from dataclasses import dataclass


@dataclass
class MarketContext:

    trend: str

    volatility: str

    session: str

    liquidity: str

    economic_event: bool

    def score(self):

        score = 100

        if self.trend != "TRENDING":
            score -= 20

        if self.volatility == "HIGH":
            score -= 15

        if self.session != "REGULAR":
            score -= 10

        if self.liquidity == "LOW":
            score -= 20

        if self.economic_event:
            score -= 35

        return max(score, 0)

    def recommendation(self):

        return "TRADE" if self.score() >= 70 else "WAIT"


if __name__ == "__main__":

    context = MarketContext(

        trend="TRENDING",

        volatility="NORMAL",

        session="REGULAR",

        liquidity="HIGH",

        economic_event=False,

    )

    print("\n================================")
    print(" STRATPILOT MARKET CONTEXT")
    print("================================")

    print(f"Trend      : {context.trend}")
    print(f"Volatility : {context.volatility}")
    print(f"Session    : {context.session}")
    print(f"Liquidity  : {context.liquidity}")
    print(f"Economic   : {context.economic_event}")

    print("\nMarket Score :", context.score())
    print("Recommendation:", context.recommendation())

    print("\nThink First. Trade Second.")
