from dataclasses import dataclass


@dataclass
class RejectionResult:
    approved: bool
    reason: str


class TradeRejectionEngine:

    def evaluate(
        self,
        trend: int,
        volatility: int,
        liquidity: int,
        session: int,
        confidence: int,
    ) -> RejectionResult:

        if trend < 70:
            return RejectionResult(False, "Trend too weak")

        if liquidity < 70:
            return RejectionResult(False, "Liquidity too low")

        if confidence < 70:
            return RejectionResult(False, "Confidence too low")

        if session < 40:
            return RejectionResult(False, "Trading session not favorable")

        if volatility < 40:
            return RejectionResult(False, "Volatility too low")

        if volatility > 95:
            return RejectionResult(False, "Volatility too high")

        return RejectionResult(True, "Trade Approved")


if __name__ == "__main__":

    engine = TradeRejectionEngine()

    result = engine.evaluate(
        trend=92,
        volatility=81,
        liquidity=94,
        session=80,
        confidence=78,
    )

    print("\n===================================")
    print("STRATPILOT TRADE REJECTION ENGINE")
    print("===================================")

    print(f"Approved : {result.approved}")
    print(f"Reason   : {result.reason}")

    print("\nThink First. Trade Second.")
