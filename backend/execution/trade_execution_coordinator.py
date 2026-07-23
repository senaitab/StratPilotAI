"""
=========================================================
StratPilot AI
Trade Execution Coordinator
Stage 37.1

Think First. Trade Second.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional

from broker.broker_adapter import BrokerAdapter
from broker.broker_models import BrokerOrder, BrokerResult


class CoordinationStatus(str, Enum):
    """Outcome of the execution-coordination process."""

    EXECUTED = "EXECUTED"
    WAIT = "WAIT"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class CoordinationResult:
    """Standard response returned by the coordinator."""

    status: CoordinationStatus
    success: bool
    message: str
    broker_result: Optional[BrokerResult] = None
    broker_order: Optional[BrokerOrder] = None


class TradeExecutionCoordinator:
    """
    Bridge between the Execution Engine and a Broker Adapter.

    Responsibilities:
    - Receive an ExecutionResult.
    - Confirm that an ExecutionPlan exists.
    - Permit only READY_TO_SEND plans.
    - Connect the selected broker when necessary.
    - Submit the plan through the broker-neutral interface.
    - Return a standardized CoordinationResult.
    """

    READY_STATUS = "READY_TO_SEND"
    CONNECTED_STATUS = "CONNECTED"

    def __init__(
        self,
        broker: BrokerAdapter,
        auto_connect: bool = True,
    ) -> None:
        if broker is None:
            raise ValueError(
                "TradeExecutionCoordinator requires a broker adapter."
            )

        self._broker = broker
        self._auto_connect = auto_connect

    @property
    def broker(self) -> BrokerAdapter:
        """Return the configured broker adapter."""

        return self._broker

    @property
    def broker_name(self) -> str:
        """Return the configured broker's display name."""

        return str(self._broker.broker_name)

    def execute(
        self,
        execution_result: Any,
    ) -> CoordinationResult:
        """
        Submit an approved ExecutionResult to the configured broker.

        The method intentionally accepts the existing ExecutionResult object
        without rebuilding it or modifying the Execution Engine.
        """

        if execution_result is None:
            return self._rejected(
                "ExecutionResult was not provided."
            )

        execution_status = self._normalize_status(
            getattr(
                execution_result,
                "status",
                "",
            )
        )

        execution_plan = getattr(
            execution_result,
            "execution_plan",
            None,
        )

        if execution_status == "WAIT":
            return CoordinationResult(
                status=CoordinationStatus.WAIT,
                success=False,
                message=(
                    "Execution paused: Execution Engine returned WAIT."
                ),
            )

        if execution_status in {
            "REJECTED",
            "FAILED",
        }:
            explanation = str(
                getattr(
                    execution_result,
                    "explanation",
                    "Execution Engine rejected the trade.",
                )
            )

            return self._rejected(
                f"Execution blocked: {explanation}"
            )

        if execution_status != self.READY_STATUS:
            return self._rejected(
                "Execution blocked: Expected ExecutionResult status "
                f"{self.READY_STATUS}, received "
                f"{execution_status or 'UNKNOWN'}."
            )

        if execution_plan is None:
            return self._rejected(
                "Execution blocked: READY_TO_SEND result has no "
                "ExecutionPlan."
            )

        plan_status = self._normalize_status(
            getattr(
                execution_plan,
                "status",
                "",
            )
        )

        if plan_status != self.READY_STATUS:
            return self._rejected(
                "Execution blocked: ExecutionPlan status must be "
                f"{self.READY_STATUS}, received "
                f"{plan_status or 'UNKNOWN'}."
            )

        connection_result = self._ensure_connected()

        if not connection_result.success:
            return CoordinationResult(
                status=CoordinationStatus.FAILED,
                success=False,
                message=(
                    "Broker connection failed: "
                    f"{connection_result.message}"
                ),
                broker_result=connection_result,
            )

        try:
            broker_result = self._broker.place_order(
                execution_plan
            )
        except Exception as exc:
            return CoordinationResult(
                status=CoordinationStatus.FAILED,
                success=False,
                message=(
                    "Broker submission raised an exception: "
                    f"{type(exc).__name__}: {exc}"
                ),
            )

        if not isinstance(
            broker_result,
            BrokerResult,
        ):
            return CoordinationResult(
                status=CoordinationStatus.FAILED,
                success=False,
                message=(
                    "Broker returned an invalid response type. "
                    "Expected BrokerResult."
                ),
            )

        if not broker_result.success:
            return CoordinationResult(
                status=CoordinationStatus.REJECTED,
                success=False,
                message=(
                    "Broker rejected the execution: "
                    f"{broker_result.message}"
                ),
                broker_result=broker_result,
                broker_order=broker_result.order,
            )

        return CoordinationResult(
            status=CoordinationStatus.EXECUTED,
            success=True,
            message=(
                f"Execution completed successfully through "
                f"{self.broker_name}: {broker_result.message}"
            ),
            broker_result=broker_result,
            broker_order=broker_result.order,
        )

    def disconnect(self) -> BrokerResult:
        """Disconnect the configured broker."""

        return self._broker.disconnect()

    def _ensure_connected(self) -> BrokerResult:
        """Connect the broker automatically when enabled."""

        connection_status = self._normalize_status(
            self._broker.connection_status
        )

        if connection_status == self.CONNECTED_STATUS:
            return BrokerResult(
                success=True,
                message=(
                    f"{self.broker_name} is already connected."
                ),
            )

        if not self._auto_connect:
            return BrokerResult(
                success=False,
                message=(
                    f"{self.broker_name} is disconnected and "
                    "automatic connection is disabled."
                ),
            )

        try:
            return self._broker.connect()
        except Exception as exc:
            return BrokerResult(
                success=False,
                message=(
                    "Broker connection raised an exception: "
                    f"{type(exc).__name__}: {exc}"
                ),
            )

    @staticmethod
    def _normalize_status(status: Any) -> str:
        """Normalize plain strings and Enum values."""

        value = getattr(
            status,
            "value",
            status,
        )

        return str(value).strip().upper()

    @staticmethod
    def _rejected(
        message: str,
    ) -> CoordinationResult:
        """Build a standardized rejected result."""

        return CoordinationResult(
            status=CoordinationStatus.REJECTED,
            success=False,
            message=message,
        )
