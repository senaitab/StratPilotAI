from dataclasses import dataclass


@dataclass
class VolatilityAnalysis:
    level: str
    atr_score: int
    vix_score: int
    overall: str


class VolatilityAnalyzer:
    def analyze(self) -> VolatilityAnalysis:
        # Placeholder values (live data will replace these later)
        atr_score = 81
        vix_score = 76

        average = (atr_score + vix_score) // 2

        if average >= 86:
            level = "EXTREME"
            overall = "AVOID"
        elif average >= 61:
            level = "HIGH"
            overall = "CAUTION"
        elif average >= 26:
            level = "NORMAL"
            overall = "GOOD"
        else:
            level = "LOW"
            overall = "QUIET"

        return VolatilityAnalysis(
            level=level,
            atr_score=atr_score,
            vix_score=vix_score,
            overall=overall,
        )


if __name__ == "__main__":
    analyzer = VolatilityAnalyzer()
    result = analyzer.analyze()

    print("\n==============================")
    print("STRATPILOT VOLATILITY ANALYZER")
    print("==============================")
    print(f"Volatility : {result.level}")
    print(f"ATR Score  : {result.atr_score}/100")
    print(f"VIX Score  : {result.vix_score}/100")
    print(f"\nOverall : {result.overall}")
    print("\nThink First. Trade Second.")
