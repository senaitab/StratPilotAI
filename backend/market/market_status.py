from datetime import datetime
from zoneinfo import ZoneInfo


class MarketStatus:
    def session(self):
        now = datetime.now(ZoneInfo("America/New_York"))

        current = now.hour * 60 + now.minute

        premarket = 4 * 60
        open_market = 9 * 60 + 30
        close_market = 16 * 60
        afterhours = 20 * 60

        if premarket <= current < open_market:
            return "PRE-MARKET"
        elif open_market <= current < close_market:
            return "REGULAR"
        elif close_market <= current < afterhours:
            return "AFTER HOURS"

        return "CLOSED"
