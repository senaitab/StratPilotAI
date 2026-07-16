from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo

from intelligence.state import IntelligenceState


@dataclass
class SessionAnalysis:
    session: str
    confidence: int
    volume: str
    momentum: str
    risk: str
    recommendation: str


class SessionAnalyzer:
    """
    Determines the current U.S. market session in Eastern Time.

    It can return a standalone SessionAnalysis object or update the
    shared IntelligenceState used by the master pipeline.
    """

    def analyze(
        self,
        state: Optional[IntelligenceState] = None,
        current_time: Optional[datetime] = None,
    ):
        eastern = ZoneInfo("America/New_York")

        if current_time is None:
            now = datetime.now(eastern)
        elif current_time.tzinfo is None:
            now = current_time.replace(tzinfo=eastern)
        else:
            now = current_time.astimezone(eastern)

        current_minutes = now.hour * 60 + now.minute

        if current_minutes < 570:
            result = SessionAnalysis(
                session="PRE_MARKET",
                confidence=40,
                volume="LOW",
                momentum="LOW",
                risk="MEDIUM",
                recommendation="WAIT",
            )

        elif current_minutes < 630:
            result = SessionAnalysis(
                session="OPENING_DRIVE",
                confidence=98,
                volume="VERY HIGH",
                momentum="VERY HIGH",
                risk="HIGH",
                recommendation="TRADE",
            )

        elif current_minutes < 690:
            result = SessionAnalysis(
                session="MID_MORNING",
                confidence=92,
                volume="HIGH",
                momentum="HIGH",
                risk="MEDIUM",
                recommendation="TRADE",
            )

        elif current_minutes < 810:
            result = SessionAnalysis(
                session="LUNCH",
                confidence=55,
                volume="LOW",
                momentum="LOW",
                risk="LOW",
                recommendation="CAUTION",
            )

        elif current_minutes < 900:
            result = SessionAnalysis(
                session="AFTERNOON",
                confidence=82,
                volume="MEDIUM",
                momentum="MEDIUM",
                risk="MEDIUM",
                recommendation="TRADE",
            )

        elif current_minutes < 960:
            result = SessionAnalysis(
                session="POWER_HOUR",
                confidence=96,
                volume="VERY HIGH",
                momentum="HIGH",
                risk="HIGH",
                recommendation="TRADE",
            )

        else:
            result = SessionAnalysis(
                session="AFTER_HOURS",
                confidence=25,
                volume="LOW",
                momentum="LOW",
                risk="LOW",
                recommendation="WAIT",
            )

        # Standalone mode.
        if state is None:
            return result

        # Shared-state pipeline mode.
        state.session_score = result.confidence
        return state


if __name__ == "__main__":
    analyzer = SessionAnalyzer()
    result = analyzer.analyze()

    print("\n==============================")
    print("STRATPILOT SESSION ANALYZER")
    print("==============================")

    print(f"Session        : {result.session}")
    print(f"Confidence     : {result.confidence}/100")
    print(f"Volume         : {result.volume}")
    print(f"Momentum       : {result.momentum}")
    print(f"Risk           : {result.risk}")
    print(f"\nRecommendation : {result.recommendation}")

    print("\nThink First. Trade Second.")
