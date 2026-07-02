from options.option_chain_adapter import OptionChainAdapter


class ContractAnalyzer:

    def __init__(self):
        self.chain = OptionChainAdapter()

    def analyze(self):

        option = self.chain.snapshot()

        spread = option["ask"] - option["bid"]

        score = 100
        reasons = []

        # Spread
        if spread > 0.20:
            score -= 15
            reasons.append("Wide bid/ask spread.")
        else:
            reasons.append("Tight bid/ask spread.")

        # Volume
        if option["volume"] < 1000:
            score -= 20
            reasons.append("Low trading volume.")
        else:
            reasons.append("Healthy volume.")

        # Open Interest
        if option["open_interest"] < 500:
            score -= 15
            reasons.append("Low open interest.")
        else:
            reasons.append("Strong open interest.")

        # Delta
        if 0.45 <= option["delta"] <= 0.65:
            reasons.append("Ideal delta.")
        else:
            score -= 10
            reasons.append("Delta outside preferred range.")

        # IV
        if option["iv"] > 60:
            score -= 10
            reasons.append("Implied volatility elevated.")
        else:
            reasons.append("IV acceptable.")

        # Theta
        if option["theta"] < -1.0:
            score -= 10
            reasons.append("High theta decay.")
        else:
            reasons.append("Theta acceptable.")

        rating = "APPROVED" if score >= 80 else "REJECT"

        return {
            "score": round(score, 2),
            "rating": rating,
            "spread": round(spread, 2),
            "reasons": reasons,
        }


if __name__ == "__main__":

    analyzer = ContractAnalyzer()

    result = analyzer.analyze()

    print()
    print("=" * 30)
    print("STRATPILOT CONTRACT ANALYZER")
    print("=" * 30)
    print()

    print(f"Rating : {result['rating']}")
    print(f"Score  : {result['score']}")
    print(f"Spread : {result['spread']}")
    print()

    print("Reasons")
    print("-" * 30)

    for reason in result["reasons"]:
        print(f"• {reason}")
