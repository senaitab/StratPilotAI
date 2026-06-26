from core.config import settings


class WebullClient:
    def __init__(self):
        self.app_key = settings.WEBULL_APP_KEY
        self.app_secret = settings.WEBULL_APP_SECRET
        self.account_id = settings.WEBULL_ACCOUNT_ID

    def status(self):
        print("=" * 40)
        print("Webull Client")

        masked_key = (
            self.app_key[:4] + "..." + self.app_key[-4:]
            if self.app_key else "Not Set"
        )

        masked_account = (
            self.account_id[:4] + "..." + self.account_id[-4:]
            if self.account_id else "Not Set"
        )

        print(f"App Key: {masked_key}")
        print(f"Account ID: {masked_account}")
        print("=" * 40)
