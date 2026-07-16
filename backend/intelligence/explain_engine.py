from dataclasses import dataclass


@dataclass
class Explanation:

    decision: str
    confidence: int
    grade: str
    recommendation: str
    reasons: list[str]


class ExplainEngine:

    def explain(
        self,
        trend: int,
        volatility: int,
        liquidity: int,
        session: int,
        confidence: int,
        risk: str,
    ) -> Explanation:

        reasons = []

        if trend >= 90:
            reasons.append("✓ Strong market trend")

        if volatility <= 85:
            reasons.append("✓ Volatility acceptable")
        else:
            reasons.append("⚠ High volatility")

        if liquidity >= 90:
            reasons.append("✓ Excellent liquidity")

        if session >= 75:
            reasons.append("✓ Trading session favorable")
        else:
            reasons.append("⚠ Weak trading session")

        if risk == "LOW":
            reasons.append("✓ Risk approved")
        elif risk == "MEDIUM":
            reasons.append("✓ Moderate risk")
        else:
            reasons.append("⚠ Elevated risk")

        if confidence >= 90:
            decision = "BUY"
            grade = "A+"
            recommendation = "EXECUTE"

        elif confidence >= 80:
            decision = "WATCH"
            grade = "A"
            recommendation = "WAIT FOR CONFIRMATION"

        else:
            decision = "WATCH"
            grade = "B"
            recommendation = "NO TRADE"

        return Explanation(
            decision,
            confidence,
            grade,
            recommendation,
            reasons,
        )


if __name__ == "__main__":

    engine = ExplainEngine()

    report = engine.explain(
        trend=92,
        volatility=81,
        liquidity=94,
        session=80,
        confidence=78,
        risk="MEDIUM",
    )

    print("\n====================================")
    print("STRATPILOT AI EXPLANATION")
    print("====================================")

    print(f"Decision       : {report.decision}")
    print(f"Confidence     : {report.confidence}")
    print(f"Grade          : {report.grade}")

    print("\nReasons")

    for reason in report.reasons:
        print(reason)

    print("\nRecommendation")
    print(report.recommendation)

    print("\nThink First. Trade Second.")
