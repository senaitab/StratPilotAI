from broker.webull_client import WebullClient


class BrokerSession:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            print("[BrokerSession] Initializing shared Webull session...")
            cls._client = WebullClient()
        return cls._client
