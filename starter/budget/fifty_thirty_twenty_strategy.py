"""Defines the 50/30/20 budget strategy."""

from budget.budget_plan import BudgetLine, BudgetPlan
from budget.budget_strategy import BudgetStrategy
from budget.budget_summary import BudgetSummary
from transaction.budget_group import BudgetGroup

# Bucket name -> (percentage of income, budget groups in the bucket).
BUCKETS: dict[str, tuple[int, tuple[BudgetGroup, ...]]] = {
    "Needs": (50, (
        BudgetGroup.HOUSING,
        BudgetGroup.GROCERIES,
        BudgetGroup.UTILITIES,
        BudgetGroup.MINIMUM_DEBT_PAYMENTS,
    )),
    "Wants": (30, (
        BudgetGroup.DINING_OUT,
        BudgetGroup.TRAVEL,
        BudgetGroup.HOBBIES,
        BudgetGroup.SUBSCRIPTIONS,
    )),
    "Savings & Debt": (20, (
        BudgetGroup.EMERGENCY_FUNDS,
        BudgetGroup.RETIREMENT,
        BudgetGroup.EXTRA_DEBT_PAYMENTS,
    )),
}


class FiftyThirtyTwentyStrategy(BudgetStrategy):
    """Splits after-tax income into 50% needs, 30% wants, 20% savings."""

    def create_plan(self, summary: BudgetSummary) -> BudgetPlan:
        lines = tuple(
            BudgetLine(
                label=f"{name} ({percent}%)",
                planned=round(summary.income * percent / 100, 2),
                actual=round(summary.spent_in(groups), 2),
            )
            for name, (percent, groups) in BUCKETS.items()
        )
        unallocated = round(
            summary.income - sum(line.planned for line in lines), 2
        )
        return BudgetPlan("50/30/20 Budget", summary.income, lines, unallocated)
