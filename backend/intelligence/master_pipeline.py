from intelligence.liquidity_analyzer import LiquidityAnalyzer
from intelligence.session_analyzer import SessionAnalyzer
from intelligence.state import IntelligenceState
from intelligence.trend_analyzer import TrendAnalyzer
from intelligence.volatility_analyzer import VolatilityAnalyzer


class MasterPipeline:
    """
    Stage 29.3 connected intelligence pipeline.

    The analyzers update one shared IntelligenceState object.
    Downstream confidence, risk, decision, and explanation values remain
    temporary until their engines are integrated in later stages.
    """

    def __init__(self):
        self.state = IntelligenceState()

        self.trend_analyzer = TrendAnalyzer()
        self.volatility_analyzer = VolatilityAnalyzer()
        self.liquidity_analyzer = LiquidityAnalyzer()
        self.session_analyzer = SessionAnalyzer()

    def run(self) -> IntelligenceState:
        print("\n====================================")
        print("STRATPILOT MASTER PIPELINE")
        print("====================================")

        print("Initializing shared intelligence state... ✓")

        # Market context remains temporary for this integration stage.
        self.state.market_context = 100

        # Real analyzer integration.
        self.state = self.trend_analyzer.analyze(self.state)
        print("[1/4] Trend Analyzer       ✓")

        self.state = self.volatility_analyzer.analyze(self.state)
        print("[2/4] Volatility Analyzer  ✓")

        self.state = self.liquidity_analyzer.analyze(self.state)
        print("[3/4] Liquidity Analyzer   ✓")

        self.state = self.session_analyzer.analyze(self.state)
        print("[4/4] Session Analyzer     ✓")

        # Temporary downstream values.
        # These will be replaced by real engine calls in future stages.
        self.state.confidence_score = round(
            (
                self.state.market_context
                + self.state.trend_score
                + self.state.volatility_score
                + self.state.liquidity_score
                + self.state.session_score
            )
            / 5
        )

        if self.state.confidence_score >= 90:
            self.state.decision = "BUY"
            self.state.grade = "A+"
            self.state.recommendation = "EXECUTE"
            self.state.risk_level = "LOW"

        elif self.state.confidence_score >= 80:
            self.state.decision = "WATCH"
            self.state.grade = "A"
            self.state.recommendation = "WAIT FOR CONFIRMATION"
            self.state.risk_level = "MEDIUM"

        elif self.state.confidence_score >= 70:
            self.state.decision = "WATCH"
            self.state.grade = "B"
            self.state.recommendation = "NO TRADE"
            self.state.risk_level = "MEDIUM"

        else:
            self.state.decision = "WAIT"
            self.state.grade = "C"
            self.state.recommendation = "NO TRADE"
            self.state.risk_level = "HIGH"

        self.state.explanation = (
            f"Trend score {self.state.trend_score}, "
            f"volatility score {self.state.volatility_score}, "
            f"liquidity score {self.state.liquidity_score}, "
            f"session score {self.state.session_score}."
        )

        print("\nShared Intelligence State")
        print(self.state)

        print("\nPipeline Status : COMPLETE")
        print("AI Status       : READY")
        print("\nThink First. Trade Second.")

        return self.state


if __name__ == "__main__":
    MasterPipeline().run()
