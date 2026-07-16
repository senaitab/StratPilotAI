from dataclasses import dataclass


@dataclass
class IntelligenceState:

    market_context: int = 0

    trend_score: int = 0
    volatility_score: int = 0
    liquidity_score: int = 0
    session_score: int = 0

    confidence_score: int = 0

    decision: str = "WAIT"
    grade: str = "-"
    recommendation: str = "WAIT"

    risk_level: str = "UNKNOWN"

    explanation: str = ""


if __name__ == "__main__":

    state = IntelligenceState()

    print("\n==============================")
    print(" STRATPILOT SHARED STATE ")
    print("==============================")

    print(state)

    print("\nThink First. Trade Second.")
