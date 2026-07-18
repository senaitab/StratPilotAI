from dataclasses import dataclass


# ---------------------------------
# INPUT
# ---------------------------------

@dataclass(frozen=True)
class TradePlan:
    confidence: int
    setup_grade: str
    contracts: int
    risk_amount: float
    status: str


# ---------------------------------
# OUTPUT
# ---------------------------------

@dataclass(frozen=True)
class ValidationResult:
    approved: bool
    execution_status: str
    explanation: str


class ExecutionValidator:

    MIN_CONFIDENCE = 70
    VALID_GRADES = {"A", "A+"}

    def analyze(
        self,
        trade: TradePlan,
    ) -> ValidationResult:

        reasons = []

        if trade.status != "READY TO EXECUTE":
            reasons.append("Trade status is not READY TO EXECUTE.")

        if trade.confidence < self.MIN_CONFIDENCE:
            reasons.append(
                f"Confidence below {self.MIN_CONFIDENCE}."
            )

        if trade.setup_grade not in self.VALID_GRADES:
            reasons.append(
                "Setup grade is below A."
            )

        if trade.contracts <= 0:
            reasons.append(
                "No contracts selected."
            )

        if trade.risk_amount <= 0:
            reasons.append(
                "Risk amount must be greater than zero."
            )

        if reasons:
            return ValidationResult(
                approved=False,
                execution_status="BLOCKED",
                explanation=" | ".join(reasons),
            )

        return ValidationResult(
            approved=True,
            execution_status="APPROVED",
            explanation=(
                "Execution passed all safety checks."
            ),
        )


def main():

    validator = ExecutionValidator()

    trade = TradePlan(
        confidence=80,
        setup_grade="A+",
        contracts=2,
        risk_amount=50.0,
        status="READY TO EXECUTE",
    )

    result = validator.analyze(trade)

    print("\n====================================")
    print("STRATPILOT EXECUTION VALIDATOR")
    print("====================================")

    print(f"\nApproved          : {result.approved}")

    print(f"Execution Status  : {result.execution_status}")

    print("\nExplanation")

    print(result.explanation)

    print("\nThink First. Trade Second.")


if __name__ == "__main__":
    main()
