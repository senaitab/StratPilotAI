from dataclasses import dataclass, field
from typing import List


@dataclass
class TradeContext:
    """
    Shared state passed between
    every StratPilot module.
    """

    symbol: str = "SPY"
    direction: str = "BUY_CALL"

    confidence: int = 0

    account_balance: float = 10000.0

    contracts: int = 0

    trade_status: str = "NEW"

    completed_modules: List[str] = field(default_factory=list)

    errors: List[str] = field(default_factory=list)

    def mark_complete(self, module_name: str):
        self.completed_modules.append(module_name)

    def add_error(self, message: str):
        self.errors.append(message)

    @property
    def successful(self):
        return len(self.errors) == 0
