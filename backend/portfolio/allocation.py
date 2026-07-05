class AllocationEngine:

    MAX_OPEN_POSITIONS = 5
    MAX_CAPITAL_USAGE_PCT = 25

    def evaluate(self, portfolio):
        buying_power = portfolio["buying_power"]
        capital_used = portfolio["capital_used"]
        open_positions = portfolio["open_positions"]

        capital_remaining = buying_power - capital_used
        capital_usage_pct = (capital_used / buying_power) * 100

        approved = (
            open_positions < self.MAX_OPEN_POSITIONS
            and capital_usage_pct < self.MAX_CAPITAL_USAGE_PCT
            and capital_remaining > 0
        )

        return {
            "approved": approved,
            "status": "APPROVED" if approved else "BLOCKED",
            "recommendation": "ALLOW" if approved else "WAIT",
            "max_position_size": 1 if approved else 0,
            "capital_remaining": round(capital_remaining, 2),
            "capital_usage_pct": round(capital_usage_pct, 2),
        }


if __name__ == "__main__":
    sample = {
        "buying_power": 36900,
        "capital_used": 1182,
        "open_positions": 2,
    }

    engine = AllocationEngine()
    print(engine.evaluate(sample))
