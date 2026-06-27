from broker.webull_client import WebullClient
from webull.data.data_client import DataClient
from webull.data.common.category import Category


class QuoteEngine:
    def __init__(self):
        self.client = WebullClient()
        self.data_client = DataClient(self.client.api_client)

    def quote(self, symbol: str):
        symbol = symbol.upper()
        res = self.data_client.market_data.get_snapshot(
            symbol,
            Category.US_STOCK.name,
            extend_hour_required=False,
overnight_required=False,
        )
        return res.json()


if __name__ == "__main__":
    q = QuoteEngine()
    print(q.quote("SPY"))
