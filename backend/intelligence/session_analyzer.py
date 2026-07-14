from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo


@dataclass
class SessionAnalysis:
    session: str
    confidence: int
    volume: str
    momentum: str
    risk: str
    recommendation: str


class SessionAnalyzer:

    def analyze(self) -> SessionAnalysis:

        eastern = ZoneInfo("America/New_York")

        now = datetime.now(eastern)

        current = now.hour * 60 + now.minute

        if current < 570:          # Before 9:30
            return SessionAnalysis(
                "PRE_MARKET",
                40,
                "LOW",
                "LOW",
                "MEDIUM",
                "WAIT"
            )

        elif current < 630:        # 9:30–10:30
            return SessionAnalysis(
                "OPENING_DRIVE",
                98,
                "VERY HIGH",
                "VERY HIGH",
                "HIGH",
                "TRADE"
            )

        elif current < 690:        # 10:30–11:30
            return SessionAnalysis(
                "MID_MORNING",
                92,
                "HIGH",
                "HIGH",
                "MEDIUM",
                "TRADE"
            )

        elif current < 810:        # 11:30–1:30
            return SessionAnalysis(
                "LUNCH",
                55,
                "LOW",
                "LOW",
                "LOW",
                "CAUTION"
            )

        elif current < 900:        # 1:30–3:00
            return SessionAnalysis(
                "AFTERNOON",
                82,
                "MEDIUM",
                "MEDIUM",
                "MEDIUM",
                "TRADE"
            )

        elif current < 960:        # 3:00–4:00
            return SessionAnalysis(
                "POWER_HOUR",
                96,
                "VERY HIGH",
                "HIGH",
                "HIGH",
                "TRADE"
            )

        return SessionAnalysis(
            "AFTER_HOURS",
            25,
            "LOW",
            "LOW",
            "LOW",
            "WAIT"
        )


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
