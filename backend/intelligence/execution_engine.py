"""
StratPilot AI - Execution Engine
Stage 35.0B: Market-Aware Execution Validation

Think First. Trade Second.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


class ExecutionStatus(str, Enum):
    READY_TO_SEND = "READY_TO_SEND"
    WAIT = "WAIT"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class MarketSnapshot:
    bid: float
    ask: float
    last: float

    @property
    def midpoint(self) -> float:
        return (self.bid + self.ask) / 2.0

    @property
    def spread(self) -> float:
        return self.ask - self.bid


@dataclass(frozen=True)
class ValidationCheck:
    name: str
    passed: bool
    message: str


@dataclass(frozen=True)
class ExecutionValidation:
    entry_deviation_percent: float
    spread: float
    estimated_slippage: float
    execution_score: int
    checks: tuple[ValidationCheck, ...]

    @property
    def validation_log(self) -> tuple[str, ...]:
        return tuple(
            f"{'PASS' if check.passed else 'FAIL'} | "
            f"{check.name} | {check.message}"
            for check in self.checks
        )


@dataclass(frozen=True)
class ExecutionPlan:
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
    execution_score: int = 0


@dataclass(frozen=True)
class ExecutionResult:
    status: ExecutionStatus
    execution_plan: Optional[ExecutionPlan]
    explanation: str
    validation: Optional[ExecutionValidation] = None


class ExecutionEngine:
    """
    Validate a TradePlan and determine whether current market conditions
    are acceptable for execution.
    """

    REQUIRED_STATUS = "READY_FOR_EXECUTION"

    MAX_ENTRY_DEVIATION = 0.01
    MAX_SPREAD = 0.10
    MAX_SLIPPAGE = 0.05

    TRADE_PLAN_POINTS = 20
    MARKET_SNAPSHOT_POINTS = 10
    ENTRY_DEVIATION_POINTS = 25
    SPREAD_POINTS = 25
    SLIPPAGE_POINTS = 20

    READY_SCORE = 95

    def analyze(
        self,
        trade_plan: Optional[Any],
        market_snapshot: Optional[MarketSnapshot] = None,
    ) -> ExecutionResult:
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

        missing = self._missing_required_fields(trade_plan)
        if missing:
            return self._rejected(
                "TradePlan is missing required fields: "
                + ", ".join(missing)
                + "."
            )

        try:
            action = str(self._read(trade_plan, "action")).strip().upper()
            symbol = str(
                self._read(trade_plan, "symbol", "underlying")
            ).strip().upper()
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

        value_error = self._validate_execution_values(
            action=action,
            symbol=symbol,
            contract=contract,
            quantity=quantity,
            planned_entry=planned_entry,
            planned_limit=planned_limit,
            stop_loss=stop_loss,
            target_1=target_1,
            target_2=target_2,
            target_3=target_3,
        )
        if value_error:
            return self._rejected(value_error)

        if market_snapshot is None:
            explanation = (
                "TradePlan passed structural validation. No MarketSnapshot "
                "was supplied, so market-aware checks were skipped and the "
                "planned entry was retained."
            )
            validation = ExecutionValidation(
                entry_deviation_percent=0.0,
                spread=0.0,
                estimated_slippage=0.0,
                execution_score=self.TRADE_PLAN_POINTS,
                checks=(
                    ValidationCheck(
                        "TradePlan",
                        True,
                        "TradePlan is structurally valid.",
                    ),
                    ValidationCheck(
                        "Market Snapshot",
                        False,
                        "No live market snapshot was supplied.",
                    ),
                ),
            )
            plan = self._create_execution_plan(
                action,
                symbol,
                contract,
                quantity,
                planned_entry,
                planned_limit,
                stop_loss,
                target_1,
                target_2,
                target_3,
                ExecutionStatus.READY_TO_SEND,
                explanation,
                validation.execution_score,
            )
            return ExecutionResult(
                ExecutionStatus.READY_TO_SEND,
                plan,
                explanation,
                validation,
            )

        snapshot_error = self._validate_snapshot(market_snapshot)
        if snapshot_error:
            return self._rejected(snapshot_error)

        midpoint = market_snapshot.midpoint
        spread = market_snapshot.spread
        deviation = abs(midpoint - planned_entry) / planned_entry
        expected_fill = min(planned_limit, market_snapshot.ask)
        slippage = max(0.0, expected_fill - midpoint)

        entry_ok = deviation <= self.MAX_ENTRY_DEVIATION
        spread_ok = spread <= self.MAX_SPREAD
        slippage_ok = slippage <= self.MAX_SLIPPAGE

        score = self.TRADE_PLAN_POINTS + self.MARKET_SNAPSHOT_POINTS
        if entry_ok:
            score += self.ENTRY_DEVIATION_POINTS
        if spread_ok:
            score += self.SPREAD_POINTS
        if slippage_ok:
            score += self.SLIPPAGE_POINTS
        score = max(0, min(100, score))

        checks = (
            ValidationCheck(
                "TradePlan",
                True,
                "Status and required fields passed.",
            ),
            ValidationCheck(
                "Market Snapshot",
                True,
                f"Bid ${market_snapshot.bid:.2f}, ask "
                f"${market_snapshot.ask:.2f}, midpoint ${midpoint:.2f}.",
            ),
            ValidationCheck(
                "Entry Deviation",
                entry_ok,
                f"{deviation * 100:.2f}% "
                f"(maximum {self.MAX_ENTRY_DEVIATION * 100:.2f}%).",
            ),
            ValidationCheck(
                "Bid/Ask Spread",
                spread_ok,
                f"${spread:.2f} (maximum ${self.MAX_SPREAD:.2f}).",
            ),
            ValidationCheck(
                "Estimated Slippage",
                slippage_ok,
                f"${slippage:.2f} (maximum ${self.MAX_SLIPPAGE:.2f}).",
            ),
        )

        validation = ExecutionValidation(
            entry_deviation_percent=round(deviation * 100.0, 4),
            spread=round(spread, 4),
            estimated_slippage=round(slippage, 4),
            execution_score=score,
            checks=checks,
        )

        ready = (
            entry_ok
            and spread_ok
            and slippage_ok
            and score >= self.READY_SCORE
        )

        if ready:
            decision = ExecutionStatus.READY_TO_SEND
            execution_entry = midpoint
            explanation = (
                "TradePlan and market-quality checks passed. "
                f"Execution score is {score}/100. "
                "ExecutionPlan is ready for the Broker Adapter."
            )
        else:
            decision = ExecutionStatus.WAIT
            execution_entry = planned_entry
            failed = ", ".join(
                check.name for check in checks if not check.passed
            )
            explanation = (
                "TradePlan is valid, but current execution quality is "
                f"unacceptable. Failed checks: {failed}. "
                f"Execution score is {score}/100. "
                "Wait for improved market conditions and analyze again."
            )

        plan = self._create_execution_plan(
            action,
            symbol,
            contract,
            quantity,
            execution_entry,
            planned_limit,
            stop_loss,
            target_1,
            target_2,
            target_3,
            decision,
            explanation,
            score,
        )

        return ExecutionResult(
            decision,
            plan,
            explanation,
            validation,
        )

    def _missing_required_fields(self, trade_plan: Any) -> list[str]:
        aliases = {
            "action": ("action",),
            "symbol": ("symbol", "underlying"),
            "contract": ("contract",),
            "entry_price": ("entry_price", "entry"),
            "limit_price": ("limit_price", "limit"),
            "stop_loss": ("stop_loss", "stop"),
            "target_1": ("target_1", "target1"),
            "target_2": ("target_2", "target2"),
            "target_3": ("target_3", "target3"),
        }
        missing: list[str] = []
        for display_name, names in aliases.items():
            value = self._read(trade_plan, *names, default=None)
            if value is None:
                missing.append(display_name)
            elif isinstance(value, str) and not value.strip():
                missing.append(display_name)
        return missing

    @staticmethod
    def _validate_execution_values(
        *,
        action: str,
        symbol: str,
        contract: str,
        quantity: int,
        planned_entry: float,
        planned_limit: float,
        stop_loss: float,
        target_1: float,
        target_2: float,
        target_3: float,
    ) -> Optional[str]:
        if not action:
            return "Execution action cannot be empty."
        if not symbol:
            return "Execution symbol cannot be empty."
        if not contract:
            return "Execution contract cannot be empty."
        if quantity <= 0:
            return "Execution quantity must be greater than zero."

        prices = {
            "entry_price": planned_entry,
            "limit_price": planned_limit,
            "stop_loss": stop_loss,
            "target_1": target_1,
            "target_2": target_2,
            "target_3": target_3,
        }
        invalid = [name for name, value in prices.items() if value <= 0]
        if invalid:
            return (
                "Execution prices must be greater than zero: "
                + ", ".join(invalid)
                + "."
            )

        if planned_limit < planned_entry:
            return (
                "Limit price cannot be below planned entry for a "
                "buy-to-open plan."
            )
        if stop_loss >= planned_entry:
            return "Stop loss must be below planned entry."
        if not (planned_entry < target_1 < target_2 < target_3):
            return (
                "Targets must be ordered: "
                "entry < target_1 < target_2 < target_3."
            )
        return None

    @staticmethod
    def _validate_snapshot(
        market_snapshot: MarketSnapshot,
    ) -> Optional[str]:
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
    def _create_execution_plan(
        action: str,
        symbol: str,
        contract: str,
        quantity: int,
        entry_price: float,
        limit_price: float,
        stop_loss: float,
        target_1: float,
        target_2: float,
        target_3: float,
        status: ExecutionStatus,
        explanation: str,
        execution_score: int,
    ) -> ExecutionPlan:
        return ExecutionPlan(
            action=action,
            symbol=symbol,
            contract=contract,
            quantity=quantity,
            entry_price=round(entry_price, 2),
            limit_price=round(limit_price, 2),
            stop_loss=round(stop_loss, 2),
            target_1=round(target_1, 2),
            target_2=round(target_2, 2),
            target_3=round(target_3, 2),
            status=status,
            explanation=explanation,
            execution_score=execution_score,
        )

    @staticmethod
    def _read(
        source: Any,
        *names: str,
        default: Any = None,
    ) -> Any:
        for name in names:
            if isinstance(source, dict) and name in source:
                return source[name]
            if hasattr(source, name):
                return getattr(source, name)
        return default

    @staticmethod
    def _status_value(status: Any) -> str:
        if isinstance(status, Enum):
            return str(status.value).strip().upper()
        return str(status).strip().upper()

    @staticmethod
    def _rejected(explanation: str) -> ExecutionResult:
        return ExecutionResult(
            ExecutionStatus.REJECTED,
            None,
            explanation,
            None,
        )

    @staticmethod
    def _failed(explanation: str) -> ExecutionResult:
        return ExecutionResult(
            ExecutionStatus.FAILED,
            None,
            explanation,
            None,
        )


@dataclass
class DemoTradePlan:
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


def _demo_plan(quantity: int = 1) -> DemoTradePlan:
    return DemoTradePlan(
        action="BUY_CALL",
        symbol="SPY",
        contract="SPY 649 CALL",
        quantity=quantity,
        entry_price=3.03,
        limit_price=3.04,
        stop_loss=2.58,
        target_1=3.48,
        target_2=3.93,
        target_3=4.38,
        status="READY_FOR_EXECUTION",
    )


def _print_result(name: str, result: ExecutionResult) -> None:
    print()
    print("=" * 68)
    print(name)
    print("=" * 68)
    print(f"Decision          : {result.status.value}")
    print(f"Explanation       : {result.explanation}")

    if result.validation:
        v = result.validation
        print(f"Execution Score   : {v.execution_score}/100")
        print(f"Entry Deviation   : {v.entry_deviation_percent:.2f}%")
        print(f"Spread            : ${v.spread:.2f}")
        print(f"Est. Slippage     : ${v.estimated_slippage:.2f}")
        print()
        print("VALIDATION LOG")
        print("-" * 68)
        for line in v.validation_log:
            print(line)

    if result.execution_plan:
        p = result.execution_plan
        print()
        print("EXECUTION PLAN")
        print("-" * 68)
        print(f"Action            : {p.action}")
        print(f"Symbol            : {p.symbol}")
        print(f"Contract          : {p.contract}")
        print(f"Quantity          : {p.quantity}")
        print(f"Entry             : ${p.entry_price:.2f}")
        print(f"Limit             : ${p.limit_price:.2f}")
        print(f"Stop              : ${p.stop_loss:.2f}")
        print(f"Target 1          : ${p.target_1:.2f}")
        print(f"Target 2          : ${p.target_2:.2f}")
        print(f"Target 3          : ${p.target_3:.2f}")
        print(f"Status            : {p.status.value}")


def _run_demo() -> None:
    engine = ExecutionEngine()

    scenarios = (
        (
            "SCENARIO 1 - IDEAL MARKET",
            _demo_plan(),
            MarketSnapshot(3.02, 3.04, 3.03),
        ),
        (
            "SCENARIO 2 - WIDE SPREAD",
            _demo_plan(),
            MarketSnapshot(2.90, 3.16, 3.03),
        ),
        (
            "SCENARIO 3 - EXCESSIVE ENTRY DEVIATION",
            _demo_plan(),
            MarketSnapshot(3.11, 3.13, 3.12),
        ),
        (
            "SCENARIO 4 - INVALID TRADE PLAN",
            _demo_plan(quantity=0),
            MarketSnapshot(3.02, 3.04, 3.03),
        ),
        (
            "SCENARIO 5 - INVALID MARKET SNAPSHOT",
            _demo_plan(),
            MarketSnapshot(3.10, 3.00, 3.05),
        ),
    )

    print("=" * 68)
    print("STRATPILOT AI EXECUTION ENGINE")
    print("STAGE 35.0B - MARKET-AWARE VALIDATION")
    print("=" * 68)

    for name, plan, snapshot in scenarios:
        _print_result(
            name,
            engine.analyze(plan, snapshot),
        )

    print()
    print("=" * 68)
    print("Think First. Trade Second. 🤝🚀")
    print("=" * 68)


if __name__ == "__main__":
    _run_demo()
