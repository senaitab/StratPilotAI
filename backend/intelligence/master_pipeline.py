from intelligence.state import IntelligenceState


class MasterPipeline:

    def __init__(self):
        self.state = IntelligenceState()

    def run(self):

        print("\n====================================")
        print(" STRATPILOT MASTER PIPELINE ")
        print("====================================")

        print("Initializing shared intelligence state... ✓")

        # Temporary values (next stages will come from real analyzers)
        self.state.market_context = 100
        self.state.trend_score = 92
        self.state.volatility_score = 81
        self.state.liquidity_score = 94
        self.state.session_score = 80
        self.state.confidence_score = 78
        self.state.risk_level = "MEDIUM"
        self.state.decision = "WATCH"
        self.state.grade = "B"
        self.state.recommendation = "NO TRADE"
        self.state.explanation = (
            "Strong trend, excellent liquidity, "
            "acceptable volatility."
        )

        print("\nShared Intelligence State\n")
        print(self.state)

        print("\nPipeline Status : COMPLETE")
        print("AI Status       : READY")

        print("\nThink First. Trade Second.")


if __name__ == "__main__":
    MasterPipeline().run()
