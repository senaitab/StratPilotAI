from options.option_chain_adapter import OptionChainAdapter


class ContractAnalyzer:

    def __init__(self):
        self.chain = OptionChainAdapter()

    def analyze_contract(self, option):

        spread = option["ask"] - option["bid"]

        score = 90
        reasons = []

        # Spread scoring
        if spread <= 0.05:
            score += 5
            reasons.append("Excellent bid/ask spread.")
        elif spread <= 0.10:
            score += 3
            reasons.append("Tight bid/ask spread.")
        elif spread <= 0.20:
            score -= 5
            reasons.append("Acceptable bid/ask spread.")
        else:
            score -= 20
            reasons.append("Wide bid/ask spread.")

        # Volume scoring
        if option["volume"] >= 20000:
            score += 5
            reasons.append("Excellent volume.")
        elif option["volume"] >= 10000:
            score += 3
            reasons.append("Healthy volume.")
        elif option["volume"] >= 5000:
            score -= 3
            reasons.append("Moderate volume.")
        else:
            score -= 20
            reasons.append("Low trading volume.")

        # Open interest scoring
        if option["open_interest"] >= 40000:
            score += 4
            reasons.append("Excellent open interest.")
        elif option["open_interest"] >= 20000:
            score += 2
            reasons.append("Strong open interest.")
        elif option["open_interest"] >= 5000:
            score -= 3
            reasons.append("Moderate open interest.")
        else:
            score -= 15
            reasons.append("Low open interest.")

        # Delta scoring
        delta = option["delta"]

        if 0.50 <= delta <= 0.58:
            score += 5
            reasons.append("Ideal delta sweet spot.")
        elif 0.45 <= delta <= 0.65:
            score += 2
            reasons.append("Acceptable delta.")
        else:
            score -= 10
            reasons.append("Delta outside preferred range.")

        # IV scoring
        iv = option["iv"]

        if iv <= 25:
            score += 3
            reasons.append("IV acceptable.")
        elif iv <= 40:
            score -= 3
            reasons.append("IV slightly elevated.")
        else:
            score -= 10
            reasons.append("IV elevated.")

        # Theta scoring
        theta = option["theta"]

        if theta >= -0.25:
            score += 3
            reasons.append("Theta acceptable.")
        elif theta >= -0.50:
            score -= 3
            reasons.append("Theta moderate.")
        else:
            score -= 10
            reasons.append("High theta decay.")

        score = max(0, min(score, 100))

        rating = "APPROVED" if score >= 80 else "REJECT"

        return {
            "score": round(score, 2),
            "rating": rating,
            "spread": round(spread, 2),
            "reasons": reasons,
        }

    def analyze(self):
        option = self.chain.snapshot()
        return self.analyze_contract(option)


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
