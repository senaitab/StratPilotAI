"""
=========================================================
StratPilot AI
Paper Broker Adapter
Stage 36.0

Think First. Trade Second.
=========================================================
"""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from typing import Any, Optional
from uuid import uuid4

from broker.broker_adapter import BrokerAdapter
from broker.broker_models import (
    BrokerConnectionStatus,
    BrokerOrder,
    BrokerOrderStatus,
    BrokerPosition,
    BrokerResult,
)


class PaperBrokerAdapter(BrokerAdapter):
    """
    Safe in-memory paper broker.

    Rules:
    - No live broker API is called.
    - Only READY_TO_SEND execution plans are accepted.
    - Accepted orders fill immediately at the limit price.
    - Orders and positions remain in memory for the current process.
    """

    BROKER_NAME = "StratPilot Paper Broker"

    def __init__(self) -> None:
        self._connection_status = BrokerConnectionStatus.DISCONNECTED
        self._orders: dict[str, BrokerOrder] = {}
        self._positions: dict[str, BrokerPosition] = {}

    @property
    def broker_name(self) -> str:
        """Return the broker display name."""

        return self.BROKER_NAME

    @property
    def connection_status(self) -> BrokerConnectionStatus:
        """Return the current connection state."""

        return self._connection_status

    def connect(self) -> BrokerResult:
        """Start the paper broker session."""

        self._connection_status = BrokerConnectionStatus.CONNECTING
        self._connection_status = BrokerConnectionStatus.CONNECTED

        return BrokerResult(
            success=True,
            message="Paper Broker connected successfully.",
        )

    def disconnect(self) -> BrokerResult:
        """End the paper broker session."""

        self._connection_status = BrokerConnectionStatus.DISCONNECTED

        return BrokerResult(
            success=True,
            message="Paper Broker disconnected successfully.",
        )

    def place_order(self, execution_plan: Any) -> BrokerResult:
        """
        Validate and simulate an immediate order fill.

        The execution plan must have status READY_TO_SEND.
        """

        if self._connection_status != BrokerConnectionStatus.CONNECTED:
            return BrokerResult(
                success=False,
                message="Order rejected: Paper Broker is not connected.",
            )

        validation_error = self._validate_execution_plan(execution_plan)

        if validation_error is not None:
            return BrokerResult(
                success=False,
                message=validation_error,
            )

        execution_status = self._normalize_status(
            execution_plan.status
        )

        if execution_status != "READY_TO_SEND":
            return BrokerResult(
                success=False,
                message=(
                    "Order rejected: ExecutionPlan status must be "
                    f"READY_TO_SEND, received {execution_status or 'UNKNOWN'}."
                ),
            )

        now = datetime.utcnow()
        order_id = f"PAPER-{uuid4().hex[:12].upper()}"

        quantity = int(execution_plan.quantity)
        limit_price = round(
            float(execution_plan.limit_price),
            2,
        )

        order = BrokerOrder(
            order_id=order_id,
            broker_name=self.BROKER_NAME,
            action=str(execution_plan.action),
            symbol=str(execution_plan.symbol),
            contract=str(execution_plan.contract),
            quantity=quantity,
            requested_price=limit_price,
            filled_quantity=quantity,
            average_fill_price=limit_price,
            status=BrokerOrderStatus.FILLED,
            created_at=now,
            updated_at=now,
            message=(
                "Paper order accepted and filled immediately "
                "at the limit price."
            ),
        )

        self._orders[order_id] = order
        self._apply_filled_order(order)

        return BrokerResult(
            success=True,
            message="Paper order accepted and filled.",
            order=order,
        )

    def cancel_order(self, order_id: str) -> BrokerResult:
        """Cancel an eligible paper order."""

        if self._connection_status != BrokerConnectionStatus.CONNECTED:
            return BrokerResult(
                success=False,
                message="Cancellation failed: Paper Broker is not connected.",
            )

        order = self._orders.get(order_id)

        if order is None:
            return BrokerResult(
                success=False,
                message=f"Cancellation failed: Order {order_id} was not found.",
            )

        if order.status == BrokerOrderStatus.FILLED:
            return BrokerResult(
                success=False,
                message="Cancellation failed: Filled orders cannot be cancelled.",
                order=order,
            )

        if order.status == BrokerOrderStatus.CANCELLED:
            return BrokerResult(
                success=False,
                message="Cancellation failed: Order is already cancelled.",
                order=order,
            )

        cancelled_order = replace(
            order,
            status=BrokerOrderStatus.CANCELLED,
            updated_at=datetime.utcnow(),
            message="Paper order cancelled.",
        )

        self._orders[order_id] = cancelled_order

        return BrokerResult(
            success=True,
            message="Paper order cancelled successfully.",
            order=cancelled_order,
        )

    def get_order_status(
        self,
        order_id: str,
    ) -> Optional[BrokerOrder]:
        """Return the current order record."""

        return self._orders.get(order_id)

    def get_positions(self) -> tuple[BrokerPosition, ...]:
        """Return all open paper positions."""

        return tuple(self._positions.values())

    def update_market_price(
        self,
        contract: str,
        market_price: float,
    ) -> BrokerResult:
        """
        Update a position's simulated market price.

        This allows Stage 36 testing of market value and unrealized P/L.
        """

        try:
            normalized_price = round(float(market_price), 2)
        except (TypeError, ValueError):
            return BrokerResult(
                success=False,
                message="Market-price update failed: Price must be numeric.",
            )

        if normalized_price <= 0:
            return BrokerResult(
                success=False,
                message=(
                    "Market-price update failed: "
                    "Price must be greater than zero."
                ),
            )

        position = self._positions.get(contract)

        if position is None:
            return BrokerResult(
                success=False,
                message=(
                    "Market-price update failed: "
                    f"No open position exists for {contract}."
                ),
            )

        self._positions[contract] = replace(
            position,
            market_price=normalized_price,
        )

        return BrokerResult(
            success=True,
            message=(
                f"Paper market price for {contract} "
                f"updated to ${normalized_price:.2f}."
            ),
        )

    def reset(self) -> BrokerResult:
        """Clear all paper orders and positions."""

        self._orders.clear()
        self._positions.clear()

        return BrokerResult(
            success=True,
            message="Paper Broker orders and positions were reset.",
        )

    def _apply_filled_order(
        self,
        order: BrokerOrder,
    ) -> None:
        """Create or update a position after a simulated fill."""

        existing_position = self._positions.get(order.contract)

        fill_quantity = int(order.filled_quantity)
        fill_price = float(order.average_fill_price or 0.0)

        if existing_position is None:
            self._positions[order.contract] = BrokerPosition(
                symbol=order.symbol,
                contract=order.contract,
                quantity=fill_quantity,
                average_price=fill_price,
                market_price=fill_price,
            )
            return

        combined_quantity = (
            existing_position.quantity
            + fill_quantity
        )

        if combined_quantity <= 0:
            self._positions.pop(
                order.contract,
                None,
            )
            return

        combined_cost = (
            existing_position.quantity
            * existing_position.average_price
            + fill_quantity
            * fill_price
        )

        average_price = round(
            combined_cost / combined_quantity,
            2,
        )

        self._positions[order.contract] = replace(
            existing_position,
            quantity=combined_quantity,
            average_price=average_price,
            market_price=fill_price,
        )

    @staticmethod
    def _validate_execution_plan(
        execution_plan: Any,
    ) -> Optional[str]:
        """Validate fields required by the Paper Broker."""

        if execution_plan is None:
            return "Order rejected: ExecutionPlan was not provided."

        required_fields = (
            "action",
            "symbol",
            "contract",
            "quantity",
            "limit_price",
            "status",
        )

        missing_fields = [
            field_name
            for field_name in required_fields
            if not hasattr(
                execution_plan,
                field_name,
            )
        ]

        if missing_fields:
            return (
                "Order rejected: ExecutionPlan is missing fields: "
                + ", ".join(missing_fields)
                + "."
            )

        if not str(execution_plan.action).strip():
            return "Order rejected: Action cannot be empty."

        if not str(execution_plan.symbol).strip():
            return "Order rejected: Symbol cannot be empty."

        if not str(execution_plan.contract).strip():
            return "Order rejected: Contract cannot be empty."

        try:
            quantity = int(execution_plan.quantity)
            limit_price = float(
                execution_plan.limit_price
            )
        except (TypeError, ValueError):
            return (
                "Order rejected: Quantity and limit price "
                "must be numeric."
            )

        if quantity <= 0:
            return "Order rejected: Quantity must be greater than zero."

        if limit_price <= 0:
            return "Order rejected: Limit price must be greater than zero."

        return None

    @staticmethod
    def _normalize_status(status: Any) -> str:
        """Normalize either an Enum or plain-string status."""

        status_value = getattr(
            status,
            "value",
            status,
        )

        return str(status_value).strip().upper()
