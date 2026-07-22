"""
=========================================================
StratPilot AI
Execution Engine
Stage 35.0A

Think First. Trade Second.
=========================================================
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


class ExecutionStatus(str, Enum):
    """Possible decisions returned by the Execution Engine."""

    READY_TO_SEND = "READY_TO_SEND"
    WAIT = "WAIT"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class MarketSnapshot:
    """
    Current option-market pricing.

    A broker or market-data adapter will populate this object
    in a later stage.
    """

    bid: float
    ask: float
    last: float

    @property
    def midpoint(self) -> float:
        """Return the bid/ask midpoint."""

        return round((self.bid + self.ask) / 2.0, 2)


@dataclass(frozen=True)
class ExecutionPlan:
    """Validated order information ready for a broker adapter."""

    action: str
    symbol: str
    contract: str

    quantity: int

    entry_price: float
    limit_price: float
    stop_loss: float

    target_1: float
    target_2: float
    target_3: float

    status: ExecutionStatus
    explanation: str


@dataclass(frozen=True)
class ExecutionResult:
    """Complete response returned by the Execution Engine."""

    status: ExecutionStatus
    execution_plan: Optional[ExecutionPlan]
    explanation: str


class ExecutionEngine:
    """
    Validate a TradePlan and convert it into an ExecutionPlan.

    Stage 35.0A validates:
    - TradePlan existence
    - TradePlan approval status
    - Required execution fields
    - Positive quantity and prices

    Market-aware spread and slippage validation will be added
    in the next stage.
    """

    REQUIRED_STATUS = "READY_FOR_EXECUTION"

    def analyze(
        self,
        trade_plan: Optional[Any],
        market_snapshot: Optional[MarketSnapshot] = None,
    ) -> ExecutionResult:
        """
        Validate a trade plan and return a structured execution result.

        The method intentionally accepts Any for the trade-plan type so it
        remains compatible with the existing StratPilot TradePlan model while
        the interfaces are being integrated.
        """

        if trade_plan is None:
            return self._rejected("TradePlan was not provided.")

        status_value = self._status_value(
            self._read(trade_plan, "status", default="")
        )

        if status_value != self.REQUIRED_STATUS:
            return self._rejected(
                "TradePlan is not approved for execution. "
                f"Received status: {status_value or 'UNKNOWN'}."
            )

        missing_fields = self._missing_required_fields(trade_plan)

        if missing_fields:
            return self._rejected(
                "TradePlan is missing required fields: "
                + ", ".join(missing_fields)
                + "."
            )

        try:
            action = str(self._read(trade_plan, "action")).strip()
            symbol = str(self._read(trade_plan, "symbol")).strip()
            contract = str(self._read(trade_plan, "contract")).strip()

            quantity = int(
                self._read(
                    trade_plan,
                    "quantity",
                    "contracts",
                    "contract_quantity",
                    default=1,
                )
            )

            planned_entry = float(
                self._read(trade_plan, "entry_price", "entry")
            )
            planned_limit = float(
                self._read(trade_plan, "limit_price", "limit")
            )
            stop_loss = float(
                self._read(trade_plan, "stop_loss", "stop")
            )

            target_1 = float(
                self._read(trade_plan, "target_1", "target1")
            )
            target_2 = float(
                self._read(trade_plan, "target_2", "target2")
            )
            target_3 = float(
                self._read(trade_plan, "target_3", "target3")
            )

        except (TypeError, ValueError) as exc:
            return self._failed(
                f"TradePlan contains invalid execution values: {exc}"
            )

        if quantity <= 0:
            return self._rejected(
                "Execution quantity must be greater than zero."
            )

        prices = {
            "entry_price": planned_entry,
            "limit_price": planned_limit,
            "stop_loss": stop_loss,
            "target_1": target_1,
            "target_2": target_2,
            "target_3": target_3,
        }

        invalid_prices = [
            name for name, value in prices.items() if value <= 0
        ]

        if invalid_prices:
            return self._rejected(
                "Execution prices must be greater than zero: "
                + ", ".join(invalid_prices)
                + "."
            )

        execution_entry = planned_entry
        explanation_lines = [
            "TradePlan status is READY_FOR_EXECUTION.",
            "Required execution fields are present.",
            "Quantity and prices passed basic validation.",
        ]

        if market_snapshot is not None:
            snapshot_error = self._validate_snapshot(market_snapshot)

            if snapshot_error:
                return self._rejected(snapshot_error)

            execution_entry = market_snapshot.midpoint
            explanation_lines.append(
                "MarketSnapshot accepted; current midpoint recorded "
                f"at {execution_entry:.2f}."
            )
        else:
            explanation_lines.append(
                "No MarketSnapshot supplied; planned entry price retained."
            )

        explanation_lines.append(
            "ExecutionPlan created and ready for the next execution layer."
        )

        explanation = " ".join(explanation_lines)

        execution_plan = ExecutionPlan(
            action=action,
            symbol=symbol,
            contract=contract,
            quantity=quantity,
            entry_price=round(execution_entry, 2),
            limit_price=round(planned_limit, 2),
            stop_loss=round(stop_loss, 2),
            target_1=round(target_1, 2),
            target_2=round(target_2, 2),
            target_3=round(target_3, 2),
            status=ExecutionStatus.READY_TO_SEND,
            explanation=explanation,
        )

        return ExecutionResult(
            status=ExecutionStatus.READY_TO_SEND,
            execution_plan=execution_plan,
            explanation=explanation,
        )

    def _missing_required_fields(self, trade_plan: Any) -> list[str]:
        """Return required fields that are absent or empty."""

        field_aliases = {
            "action": ("action",),
            "symbol": ("symbol",),
            "contract": ("contract",),
            "entry_price": ("entry_price", "entry"),
            "limit_price": ("limit_price", "limit"),
            "stop_loss": ("stop_loss", "stop"),
            "target_1": ("target_1", "target1"),
            "target_2": ("target_2", "target2"),
            "target_3": ("target_3", "target3"),
        }

        missing: list[str] = []

        for display_name, aliases in field_aliases.items():
            value = self._read(
                trade_plan,
                *aliases,
                default=None,
            )

            if value is None:
                missing.append(display_name)
            elif isinstance(value, str) and not value.strip():
                missing.append(display_name)

        return missing

    @staticmethod
    def _validate_snapshot(
        market_snapshot: MarketSnapshot,
    ) -> Optional[str]:
        """Validate basic bid, ask, and last-price relationships."""

        if market_snapshot.bid <= 0:
            return "MarketSnapshot bid must be greater than zero."

        if market_snapshot.ask <= 0:
            return "MarketSnapshot ask must be greater than zero."

        if market_snapshot.last <= 0:
            return "MarketSnapshot last price must be greater than zero."

        if market_snapshot.ask < market_snapshot.bid:
            return "MarketSnapshot ask cannot be below the bid."

        return None

    @staticmethod
    def _read(
        source: Any,
        *names: str,
        default: Any = None,
    ) -> Any:
        """
        Read the first matching value from an object or dictionary.

        This compatibility helper lets the engine consume either dataclasses,
        normal objects, or dictionaries.
        """

        for name in names:
            if isinstance(source, dict) and name in source:
                return source[name]

            if hasattr(source, name):
                return getattr(source, name)

        return default

    @staticmethod
    def _status_value(status: Any) -> str:
        """Normalize plain strings and Enum status values."""

        if isinstance(status, Enum):
            return str(status.value).strip().upper()

        return str(status).strip().upper()

    @staticmethod
    def _rejected(explanation: str) -> ExecutionResult:
        return ExecutionResult(
            status=ExecutionStatus.REJECTED,
            execution_plan=None,
            explanation=explanation,
        )

    @staticmethod
    def _failed(explanation: str) -> ExecutionResult:
        return ExecutionResult(
            status=ExecutionStatus.FAILED,
            execution_plan=None,
            explanation=explanation,
        )


@dataclass
class DemoTradePlan:
    """Standalone test model used only by this module's demo."""

    action: str
    symbol: str
    contract: str
    quantity: int

    entry_price: float
    limit_price: float
    stop_loss: float

    target_1: float
    target_2: float
    target_3: float

    status: str


def _run_demo() -> None:
    """Run a deterministic Stage 35.0A smoke test."""

    trade_plan = DemoTradePlan(
        action="BUY_CALL",
        symbol="SPY",
        contract="SPY 649 CALL",
        quantity=1,
        entry_price=3.03,
        limit_price=3.04,
        stop_loss=2.58,
        target_1=3.48,
        target_2=3.93,
        target_3=4.38,
        status="READY_FOR_EXECUTION",
    )

    market_snapshot = MarketSnapshot(
        bid=3.02,
        ask=3.04,
        last=3.03,
    )

    engine = ExecutionEngine()
    result = engine.analyze(
        trade_plan=trade_plan,
        market_snapshot=market_snapshot,
    )

    print("=" * 58)
    print("STRATPILOT EXECUTION ENGINE")
    print("STAGE 35.0A")
    print("=" * 58)
    print()
    print(f"Execution Status : {result.status.value}")
    print(f"Explanation      : {result.explanation}")

    if result.execution_plan is None:
        print()
        print("No ExecutionPlan was created.")
        return

    plan = result.execution_plan

    print()
    print("EXECUTION PLAN")
    print("-" * 58)
    print(f"Action           : {plan.action}")
    print(f"Symbol           : {plan.symbol}")
    print(f"Contract         : {plan.contract}")
    print(f"Quantity         : {plan.quantity}")
    print(f"Entry            : {plan.entry_price:.2f}")
    print(f"Limit            : {plan.limit_price:.2f}")
    print(f"Stop             : {plan.stop_loss:.2f}")
    print(f"Target 1         : {plan.target_1:.2f}")
    print(f"Target 2         : {plan.target_2:.2f}")
    print(f"Target 3         : {plan.target_3:.2f}")
    print(f"Status           : {plan.status.value}")
    print()
    print("Think First. Trade Second. 🤝🚀")


if __name__ == "__main__":
    _run_demo()
