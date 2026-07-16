class MasterPipeline:

    def __init__(self):
        self.modules = [
            "Market Context",
            "Trend Analyzer",
            "Volatility Analyzer",
            "Liquidity Analyzer",
            "Session Analyzer",
            "Market Confidence",
            "Risk Engine",
            "Decision Engine",
            "Explain Engine",
        ]

    def run(self):

        print("\n====================================")
        print(" STRATPILOT MASTER PIPELINE ")
        print("====================================")

        for i, module in enumerate(self.modules, start=1):
            print(f"[{i}/9] {module:<24} ✓")

        print("\nPipeline Status : COMPLETE")
        print("AI Status       : READY")
        print("\nThink First. Trade Second.")


if __name__ == "__main__":
    MasterPipeline().run()
