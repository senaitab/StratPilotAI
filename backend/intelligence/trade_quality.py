from dataclasses import dataclass


@dataclass
class TradeQuality:
    score: int
    stars: int
    grade: str
    recommendation: str


class TradeQualityEngine:

    def evaluate(self, score: int) -> TradeQuality:

        if score >= 95:
            return TradeQuality(score, 5, "A+", "EXECUTE")

        elif score >= 90:
            return TradeQuality(score, 5, "A", "EXECUTE")

        elif score >= 80:
            return TradeQuality(score, 4, "B+", "WATCH")

        elif score >= 70:
            return TradeQuality(score, 3, "B", "WATCH")

        elif score >= 60:
            return TradeQuality(score, 2, "C", "WAIT")

        else:
            return TradeQuality(score, 1, "F", "REJECT")


if __name__ == "__main__":

    engine = TradeQualityEngine()

    trade = engine.evaluate(78)

    print("\n================================")
    print("STRATPILOT TRADE QUALITY")
    print("================================")

    print(f"Score          : {trade.score}")
    print(f"Stars          : {'★' * trade.stars}")
    print(f"Grade          : {trade.grade}")
    print(f"Recommendation : {trade.recommendation}")

    print("\nThink First. Trade Second.")
