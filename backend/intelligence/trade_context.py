from dataclasses import dataclass, field
from typing import List


@dataclass
class TradeContext:
    """
    Shared trade state used by the StratPilot AI pipeline.
    """

    # Trade identity
    symbol: str = "SPY"
    direction: str = ""
    trade_status: str = "NEW"

    # Decision Engine output
    confidence: int = 0
    setup_grade: str = ""
    decision_risk_level: str = ""
    decision_explanation: str = ""

    # Risk Manager output
    risk_level: str = ""
    risk_multiplier: float = 0.0
    trade_allowed: bool = False
    risk_explanation: str = ""

    # Account and sizing fields for later stages
    account_balance: float = 10000.0
    contracts: int = 0

    # Pipeline tracking
    completed_modules: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def mark_complete(self, module_name: str) -> None:
        if module_name not in self.completed_modules:
            self.completed_modules.append(module_name)

    def add_error(self, message: str) -> None:
        self.errors.append(message)
        self.trade_status = "FAILED"

    @property
    def successful(self) -> bool:
        return not self.errors
