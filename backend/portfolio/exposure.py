class ExposureEngine:

    def calculate(self):
        return {
            "delta": 0.61,
            "theta": -0.25,
            "gamma": 0.08,
            "vega": 0.14,
            "risk": "LOW",
        }


if __name__ == "__main__":
    engine = ExposureEngine()
    print(engine.calculate())
