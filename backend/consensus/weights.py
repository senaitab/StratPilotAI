class DynamicWeights:

    def get(self, regime):

        if regime == "BULL":
            return {
                "market": 35,
                "risk": 20,
                "strategy": 25,
                "options": 10,
                "position": 5,
                "portfolio": 5,
            }

        if regime == "BEAR":
            return {
                "market": 20,
                "risk": 40,
                "strategy": 15,
                "options": 5,
                "position": 10,
                "portfolio": 10,
            }

        if regime == "RANGE":
            return {
                "market": 20,
                "risk": 25,
                "strategy": 30,
                "options": 10,
                "position": 10,
                "portfolio": 5,
            }

        return {
            "market": 30,
            "risk": 25,
            "strategy": 20,
            "options": 10,
            "position": 10,
            "portfolio": 5,
        }


if __name__ == "__main__":

    engine = DynamicWeights()

    for regime in ["BULL", "BEAR", "RANGE", "NORMAL"]:
        print(f"\n{regime}")
        print(engine.get(regime))
