from dataclasses import dataclass


@dataclass
class DecisionResult:
    score: int
    grade: str
    confidence: str
    action: str
    reason: str


class DecisionEngine:

    def evaluate(self, confidence_score: int) -> DecisionResult:

        if confidence_score >= 95:
            return DecisionResult(
                95,
                "A+",
                "VERY HIGH",
                "BUY",
                "Institutional-quality setup."
            )

        elif confidence_score >= 85:
            return DecisionResult(
                confidence_score,
                "A",
                "HIGH",
                "BUY",
                "Strong setup approved."
            )

        elif confidence_score >= 75:
            return DecisionResult(
                confidence_score,
                "B",
                "MEDIUM",
                "WATCH",
                "Conditions are acceptable, but not ideal."
            )

        else:
            return DecisionResult(
                confidence_score,
                "C",
                "LOW",
                "WAIT",
                "Market conditions are not favorable."
            )


if __name__ == "__main__":

    engine = DecisionEngine()

    result = engine.evaluate(78)

    print("\n===================================")
    print("STRATPILOT DECISION ENGINE")
    print("===================================")

    print(f"Decision Score : {result.score}")
    print(f"Grade          : {result.grade}")
    print(f"Confidence     : {result.confidence}")
    print(f"Action         : {result.action}")

    print("\nReason")
    print(result.reason)

    print("\nThink First. Trade Second.")
