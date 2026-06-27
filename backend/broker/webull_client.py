from core.config import settings
from webull.core.client import ApiClient
from webull.trade.trade_client import TradeClient


class WebullClient:
    def __init__(self):
        self.app_key = settings.WEBULL_APP_KEY
        self.app_secret = settings.WEBULL_APP_SECRET
        self.account_id = settings.WEBULL_ACCOUNT_ID

        self.api_client = ApiClient(self.app_key, self.app_secret, "us")
        self.api_client.add_endpoint("us", "api.webull.com")
        self.trade_client = TradeClient(self.api_client)

    def status(self):
        print("Webull Client Connected")
        print(f"Account ID: {self.account_id[:4]}...{self.account_id[-4:]}")

    def get_accounts(self):
        return self.trade_client.account_v2.get_account_list().json()

    def get_balance(self):
        return self.trade_client.account_v2.get_account_balance(self.account_id).json()

    def get_positions(self):
        return self.trade_client.account_v2.get_account_position(self.account_id).json()
