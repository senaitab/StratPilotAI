"""
=========================================================
StratPilot AI
Broker Adapter Interface
Stage 36.0

Think First. Trade Second.
=========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Optional

from broker.broker_models import (
    BrokerConnectionStatus,
    BrokerOrder,
    BrokerPosition,
    BrokerResult,
)


class BrokerAdapter(ABC):
    """
    Broker-neutral interface implemented by every broker adapter.

    The Execution Engine and Trade Execution Coordinator communicate
    through this interface rather than importing broker-specific code.
    """

    @property
    @abstractmethod
    def broker_name(self) -> str:
        """Return the broker display name."""

    @property
    @abstractmethod
    def connection_status(self) -> BrokerConnectionStatus:
        """Return the current broker connection state."""

    @abstractmethod
    def connect(self) -> BrokerResult:
        """Connect or initialize the broker session."""

    @abstractmethod
    def disconnect(self) -> BrokerResult:
        """Disconnect or close the broker session."""

    @abstractmethod
    def place_order(
        self,
        execution_plan: Any,
    ) -> BrokerResult:
        """Submit a validated ExecutionPlan."""

    @abstractmethod
    def cancel_order(
        self,
        order_id: str,
    ) -> BrokerResult:
        """Cancel an eligible broker order."""

    @abstractmethod
    def get_order_status(
        self,
        order_id: str,
    ) -> Optional[BrokerOrder]:
        """Return the latest state of a broker order."""

    @abstractmethod
    def get_positions(
        self,
    ) -> tuple[BrokerPosition, ...]:
        """Return all currently open broker positions."""
