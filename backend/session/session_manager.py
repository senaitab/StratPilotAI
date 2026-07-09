from datetime import datetime


class SessionManager:

    def __init__(self):
        self.now = datetime.now()

    def evaluate(self):

        weekday = self.now.weekday()  # Monday = 0
        hour = self.now.hour
        minute = self.now.minute

        weekend = weekday >= 5

        current_minutes = hour * 60 + minute

        premarket = 4 * 60 <= current_minutes < 9 * 60 + 30
        market = 9 * 60 + 30 <= current_minutes < 16 * 60
        afterhours = 16 * 60 <= current_minutes < 20 * 60

        if weekend:
            session = "CLOSED"
            allowed = False
        elif market:
            session = "MARKET"
            allowed = True
        elif premarket:
            session = "PREMARKET"
            allowed = False
        elif afterhours:
            session = "AFTER HOURS"
            allowed = False
        else:
            session = "CLOSED"
            allowed = False

        return {
            "timestamp": self.now.strftime("%Y-%m-%d %H:%M:%S"),
            "session": session,
            "market_open": market,
            "trading_allowed": allowed,
        }


if __name__ == "__main__":

    manager = SessionManager()
    report = manager.evaluate()

    print("\n==============================")
    print(" STRATPILOT SESSION MANAGER")
    print("==============================")

    print(f"Time             : {report['timestamp']}")
    print(f"Session          : {report['session']}")
    print(f"Market Open      : {report['market_open']}")
    print(f"Trading Allowed  : {report['trading_allowed']}")

    print("\nThink First. Trade Second.")
