from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from intelligence.trade_planner import TradePlan


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

    # Position Sizer output
    account_balance: float = 10000.0
    base_risk_percent: float = 0.0
    effective_risk_percent: float = 0.0
    risk_amount: float = 0.0
    risk_per_contract: float = 0.0
    contracts: int = 0
    position_explanation: str = ""

    # Contract Selector output
    selected_symbol: str = ""
    selected_option_type: str = ""
    selected_strike: float = 0.0
    selected_expiration: str = ""
    selected_delta: float = 0.0
    liquidity_score: int = 0
    overall_score: int = 0
    contract_explanation: str = ""
    # Trade Planner output
    trade_plan: Optional["TradePlan"] = None
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
