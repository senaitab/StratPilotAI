from intelligence.market_data_provider import MarketData


class TrendAnalyzer:
    """
    Stage 30.1

    Trend analysis using MarketData.
    Placeholder logic for now.
    """

    def analyze(self, market: MarketData) -> int:

        score = 50

        if market.price > market.open_price:
            score += 20

        if market.price > market.previous_close:
            score += 20

        if market.high > market.open_price:
            score += 10

        return min(score, 100)


if __name__ == "__main__":

    from intelligence.market_data_provider import MarketDataProvider

    provider = MarketDataProvider()

    market = provider.get_market_data()

    analyzer = TrendAnalyzer()

    score = analyzer.analyze(market)

    print("\n==============================")
    print(" STRATPILOT TREND ANALYZER")
    print("==============================")

    print(f"Price : {market.price}")
    print(f"Open  : {market.open_price}")
    print(f"Trend Score : {score}/100")

    if score >= 80:
        print("Trend : STRONG")
    elif score >= 60:
        print("Trend : MODERATE")
    else:
        print("Trend : WEAK")

    print("\nThink First. Trade Second.")
