from dataclasses import dataclass


@dataclass
class LiquidityAnalysis:
    level: str
    volume_score: int
    spread_score: int
    overall: str


class LiquidityAnalyzer:
    def analyze(self) -> LiquidityAnalysis:
        # Placeholder values (live market data will replace these later)
        volume_score = 94
        spread_score = 91

        average = (volume_score + spread_score) // 2

        if average >= 86:
            level = "EXCELLENT"
            overall = "TRADE"
        elif average >= 61:
            level = "GOOD"
            overall = "FAVORABLE"
        elif average >= 26:
            level = "FAIR"
            overall = "CAUTION"
        else:
            level = "POOR"
            overall = "AVOID"

        return LiquidityAnalysis(
            level=level,
            volume_score=volume_score,
            spread_score=spread_score,
            overall=overall,
        )


if __name__ == "__main__":
    analyzer = LiquidityAnalyzer()
    result = analyzer.analyze()

    print("\n==============================")
    print("STRATPILOT LIQUIDITY ANALYZER")
    print("==============================")
    print(f"Liquidity   : {result.level}")
    print(f"Volume      : {result.volume_score}/100")
    print(f"Spread      : {result.spread_score}/100")
    print(f"\nOverall : {result.overall}")
    print("\nThink First. Trade Second.")
