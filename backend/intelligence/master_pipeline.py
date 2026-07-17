from intelligence.liquidity_analyzer import LiquidityAnalyzer
from intelligence.market_data_provider import (
    MarketData,
    MarketDataProvider,
)
from intelligence.session_analyzer import SessionAnalyzer
from intelligence.state import IntelligenceState
from intelligence.trend_analyzer import TrendAnalyzer
from intelligence.volatility_analyzer import VolatilityAnalyzer


class MasterPipeline:
    """
    Stage 30.5 — Unified Market Intelligence Pipeline

    Responsibilities:
    1. Fetch one synchronized MarketData snapshot.
    2. Pass that same snapshot to every analyzer.
    3. Collect analyzer results.
    4. Populate one shared IntelligenceState.
    5. Calculate confidence, decision, risk, and explanation.
    """

    def __init__(self, symbol: str = "SPY") -> None:
        self.symbol = symbol.upper()

        self.market_provider = MarketDataProvider()
        self.trend_analyzer = TrendAnalyzer()
        self.volatility_analyzer = VolatilityAnalyzer()
        self.liquidity_analyzer = LiquidityAnalyzer()
        self.session_analyzer = SessionAnalyzer()

        self.state = IntelligenceState()

    def run(self) -> IntelligenceState:
        print("\n========================================")
        print("STRATPILOT MASTER INTELLIGENCE PIPELINE")
        print("========================================")

        # ---------------------------------------------------------
        # 1. Load one synchronized market snapshot
        # ---------------------------------------------------------
        market = self.market_provider.get_market_data(self.symbol)
        self._validate_market_data(market)

        print("\nLoading synchronized market data... ✓")
        print(f"Symbol           : {market.symbol}")
        print(f"Price            : ${market.price:.2f}")
        print(
            "Timestamp        : "
            f"{market.timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        )

        # ---------------------------------------------------------
        # 2. Run analyzers using the same MarketData object
        # ---------------------------------------------------------
        trend_score = self.trend_analyzer.analyze(market)
        print("[1/4] Trend Analyzer       ✓")

        volatility_result = self.volatility_analyzer.analyze(market)
        print("[2/4] Volatility Analyzer  ✓")

        liquidity_result = self.liquidity_analyzer.analyze(market)
        print("[3/4] Liquidity Analyzer   ✓")

        session_result = self.session_analyzer.analyze(market)
        print("[4/4] Session Analyzer     ✓")

        # ---------------------------------------------------------
        # 3. Populate shared IntelligenceState
        # ---------------------------------------------------------
        self.state.market_context = self._calculate_market_context(market)
        self.state.trend_score = trend_score
        self.state.volatility_score = volatility_result.score
        self.state.liquidity_score = liquidity_result.score
        self.state.session_score = session_result.score

        # ---------------------------------------------------------
        # 4. Calculate overall confidence
        # ---------------------------------------------------------
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

        # ---------------------------------------------------------
        # 5. Produce decision, grade, risk, and recommendation
        # ---------------------------------------------------------
        self._apply_decision_logic()
        self._build_explanation(
            market=market,
            volatility_status=volatility_result.status,
            liquidity_status=liquidity_result.status,
            session_name=session_result.session,
        )

        # ---------------------------------------------------------
        # 6. Print consolidated report
        # ---------------------------------------------------------
        self._print_report(
            market=market,
            volatility_status=volatility_result.status,
            liquidity_status=liquidity_result.status,
            session_name=session_result.session,
        )

        return self.state

    def _calculate_market_context(self, market: MarketData) -> int:
        """
        Temporary Stage 30.5 market-context calculation.

        Later stages can replace this with EMA, VWAP, breadth,
        economic-event, and higher-timeframe market context.
        """
        score = 50

        if market.price > market.open_price:
            score += 15

        if market.price > market.previous_close:
            score += 15

        if market.high > market.previous_close:
            score += 10

        if market.volume >= 100_000_000:
            score += 10

        return min(score, 100)

    def _apply_decision_logic(self) -> None:
        confidence = self.state.confidence_score

        # Critical safety guard:
        # Never approve execution when the session is unfavorable.
        poor_session = self.state.session_score < 60

        if poor_session:
            self.state.decision = "WAIT"
            self.state.grade = "C"
            self.state.recommendation = "NO TRADE"
            self.state.risk_level = "HIGH"
            return

        if confidence >= 90:
            self.state.decision = "BUY"
            self.state.grade = "A+"
            self.state.recommendation = "EXECUTE"
            self.state.risk_level = "LOW"

        elif confidence >= 80:
            self.state.decision = "WATCH"
            self.state.grade = "A"
            self.state.recommendation = "WAIT FOR CONFIRMATION"
            self.state.risk_level = "MEDIUM"

        elif confidence >= 70:
            self.state.decision = "WATCH"
            self.state.grade = "B"
            self.state.recommendation = "NO TRADE"
            self.state.risk_level = "MEDIUM"

        else:
            self.state.decision = "WAIT"
            self.state.grade = "C"
            self.state.recommendation = "NO TRADE"
            self.state.risk_level = "HIGH"

    def _build_explanation(
        self,
        market: MarketData,
        volatility_status: str,
        liquidity_status: str,
        session_name: str,
    ) -> None:
        self.state.explanation = (
            f"{market.symbol} market snapshot: "
            f"price ${market.price:.2f}, "
            f"trend {self.state.trend_score}/100, "
            f"volatility {self.state.volatility_score}/100 "
            f"({volatility_status}), "
            f"liquidity {self.state.liquidity_score}/100 "
            f"({liquidity_status}), "
            f"session {session_name} "
            f"({self.state.session_score}/100), "
            f"overall confidence "
            f"{self.state.confidence_score}/100."
        )

    def _print_report(
        self,
        market: MarketData,
        volatility_status: str,
        liquidity_status: str,
        session_name: str,
    ) -> None:
        print("\n----------------------------------------")
        print("MARKET INTELLIGENCE REPORT")
        print("----------------------------------------")

        print(f"Symbol             : {market.symbol}")
        print(f"Price              : ${market.price:.2f}")
        print(f"Open               : ${market.open_price:.2f}")
        print(f"High               : ${market.high:.2f}")
        print(f"Low                : ${market.low:.2f}")
        print(f"Previous Close     : ${market.previous_close:.2f}")
        print(f"Volume             : {market.volume:,}")

        print("\n----------------------------------------")
        print("SHARED INTELLIGENCE STATE")
        print("----------------------------------------")

        print(
            f"Market Context     : "
            f"{self.state.market_context}/100"
        )
        print(
            f"Trend Score        : "
            f"{self.state.trend_score}/100"
        )
        print(
            f"Volatility Score   : "
            f"{self.state.volatility_score}/100 "
            f"({volatility_status})"
        )
        print(
            f"Liquidity Score    : "
            f"{self.state.liquidity_score}/100 "
            f"({liquidity_status})"
        )
        print(
            f"Session Score      : "
            f"{self.state.session_score}/100 "
            f"({session_name})"
        )

        print("\n----------------------------------------")
        print("FINAL AI DECISION")
        print("----------------------------------------")

        print(
            f"Confidence         : "
            f"{self.state.confidence_score}/100"
        )
        print(f"Decision           : {self.state.decision}")
        print(f"Grade              : {self.state.grade}")
        print(f"Risk Level         : {self.state.risk_level}")
        print(
            f"Recommendation     : "
            f"{self.state.recommendation}"
        )

        print("\nExplanation")
        print(self.state.explanation)

        print("\nPipeline Status    : COMPLETE")
        print("AI Status          : READY")
        print("\nThink First. Trade Second.")

    @staticmethod
    def _validate_market_data(market: MarketData) -> None:
        if market.price <= 0:
            raise ValueError(
                "Market price must be greater than zero."
            )

        if market.open_price <= 0:
            raise ValueError(
                "Market open price must be greater than zero."
            )

        if market.previous_close <= 0:
            raise ValueError(
                "Previous close must be greater than zero."
            )

        if market.high < market.low:
            raise ValueError(
                "Market high cannot be lower than market low."
            )

        if not market.low <= market.price <= market.high:
            raise ValueError(
                "Current price must be between market low and high."
            )

        if market.volume < 0:
            raise ValueError(
                "Market volume cannot be negative."
            )


if __name__ == "__main__":
    pipeline = MasterPipeline(symbol="SPY")
    pipeline.run()
