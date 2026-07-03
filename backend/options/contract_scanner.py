from options.contract_analyzer import ContractAnalyzer


class ContractScanner:

    def __init__(self):
        self.analyzer = ContractAnalyzer()

    def scan(self):
        candidates = [
            {
                "symbol": "SPY",
                "expiration": "2026-07-02",
                "strike": 731,
                "type": "CALL",
                "bid": 5.72,
                "ask": 5.80,
                "volume": 14500,
                "open_interest": 38100,
                "iv": 18.9,
                "delta": 0.61,
                "theta": -0.25,
            },
            {
                "symbol": "SPY",
                "expiration": "2026-07-02",
                "strike": 732,
                "type": "CALL",
                "bid": 5.18,
                "ask": 5.24,
                "volume": 18245,
                "open_interest": 40218,
                "iv": 18.7,
                "delta": 0.54,
                "theta": -0.23,
            },
            {
                "symbol": "SPY",
                "expiration": "2026-07-02",
                "strike": 733,
                "type": "CALL",
                "bid": 4.62,
                "ask": 4.80,
                "volume": 8200,
                "open_interest": 22100,
                "iv": 19.4,
                "delta": 0.47,
                "theta": -0.29,
            },
        ]

        ranked = []

        for contract in candidates:
            result = self.analyzer.analyze_contract(contract)

            ranked.append({
                "contract": contract,
                "score": result["score"],
                "rating": result["rating"],
                "spread": result["spread"],
                "reasons": result["reasons"],
            })

        ranked.sort(key=lambda x: x["score"], reverse=True)

        return {
            "recommended": ranked[0],
            "ranked": ranked,
        }


if __name__ == "__main__":

    scanner = ContractScanner()
    result = scanner.scan()

    print()
    print("=" * 30)
    print("STRATPILOT CONTRACT SCANNER")
    print("=" * 30)
    print()

    print("Top Contract Candidates")
    print("-" * 30)

    for i, item in enumerate(result["ranked"], start=1):
        c = item["contract"]

        print(
            f"{i}. {c['symbol']} {c['strike']} {c['type']} "
            f"{c['expiration']} | Score: {item['score']} | "
            f"Rating: {item['rating']} | Spread: {item['spread']}"
        )

    best = result["recommended"]["contract"]

    print()
    print("Recommended Contract")
    print("-" * 30)
    print(f"{best['symbol']} {best['strike']} {best['type']} {best['expiration']}")

    print()
    print("Think First. Trade Second.")
