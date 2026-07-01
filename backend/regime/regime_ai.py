class RegimeAI:
    def detect(self, market):

        change = market["change_pct"]

        if abs(change) < 0.30:
            return "RANGE"

        if change > 1.0:
            return "BULL"

        if change < -1.0:
            return "BEAR"

        return "NORMAL"


if __name__ == "__main__":

    ai = RegimeAI()

    tests = [
        {"change_pct":0.05},
        {"change_pct":1.8},
        {"change_pct":-2.4},
        {"change_pct":0.6},
    ]

    for t in tests:
        print(ai.detect(t))
