"""
=========================================================
StratPilot AI
Broker Models
Stage 36.0

Think First. Trade Second.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class BrokerConnectionStatus(str, Enum):
    """Current broker connection state."""

    DISCONNECTED = "DISCONNECTED"
    CONNECTING = "CONNECTING"
    CONNECTED = "CONNECTED"
    ERROR = "ERROR"


class BrokerOrderStatus(str, Enum):
    """Current broker order state."""

    CREATED = "CREATED"
    SUBMITTED = "SUBMITTED"
    ACCEPTED = "ACCEPTED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
    ERROR = "ERROR"


@dataclass(frozen=True)
class BrokerOrder:
    """
    Broker-neutral order object.

    Every broker (Paper, Webull, IBKR, etc.)
    will translate into this format.
    """

    order_id: str
    broker_name: str

    action: str
    symbol: str
    contract: str

    quantity: int

    requested_price: float

    filled_quantity: int = 0
    average_fill_price: Optional[float] = None

    status: BrokerOrderStatus = BrokerOrderStatus.CREATED

    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

    message: str = ""


@dataclass(frozen=True)
class BrokerPosition:
    """
    Standard open position.
    """

    symbol: str
    contract: str

    quantity: int

    average_price: float

    market_price: float

    @property
    def market_value(self) -> float:
        return round(
            self.quantity * self.market_price * 100,
            2,
        )

    @property
    def unrealized_pl(self) -> float:
        return round(
            (self.market_price - self.average_price)
            * self.quantity
            * 100,
            2,
        )


@dataclass(frozen=True)
class BrokerResult:
    """
    Standard response returned
    from every Broker Adapter.
    """

    success: bool

    message: str

    order: Optional[BrokerOrder] = None
