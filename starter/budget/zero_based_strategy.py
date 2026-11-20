"""Defines the zero-based budget strategy."""

from budget.budget_plan import BudgetLine, BudgetPlan
from budget.budget_strategy import BudgetStrategy
from budget.budget_summary import BudgetSummary
from transaction.budget_group import BudgetGroup

# Default share of income (%) given to each budget group; totals 100.
DEFAULT_PERCENTAGES: dict[BudgetGroup, int] = {
    BudgetGroup.HOUSING: 25,
    BudgetGroup.GROCERIES: 12,
    BudgetGroup.UTILITIES: 8,
    BudgetGroup.MINIMUM_DEBT_PAYMENTS: 5,
    BudgetGroup.DINING_OUT: 8,
    BudgetGroup.TRAVEL: 8,
    BudgetGroup.HOBBIES: 6,
    BudgetGroup.SUBSCRIPTIONS: 8,
    BudgetGroup.EMERGENCY_FUNDS: 8,
    BudgetGroup.RETIREMENT: 7,
    BudgetGroup.EXTRA_DEBT_PAYMENTS: 5,
}


class ZeroBasedStrategy(BudgetStrategy):
    """Assigns every dollar of income to a specific budget group.

    By default income is shared out using DEFAULT_PERCENTAGES, with any
    rounding difference added to the largest group so nothing is left over.
    Passing explicit amounts per group uses them as given, and any income
    they do not cover is reported as unallocated.
    """

    def __init__(self, allocations: dict[BudgetGroup, float] | None = None):
        self.allocations = allocations

    def create_plan(self, summary: BudgetSummary) -> BudgetPlan:
        if self.allocations is None:
            planned = self._by_percentage(summary.income)
        else:
            planned = {
                group: self.allocations.get(group, 0.0)
                for group in BudgetGroup
            }
        lines = tuple(
            BudgetLine(
                group.value, round(planned[group], 2),
                round(summary.spending[group], 2),
            )
            for group in BudgetGroup
        )
        unallocated = round(summary.income - sum(planned.values()), 2)
        return BudgetPlan(
            "Zero-Based Budget", summary.income, lines, unallocated,
            round(summary.uncategorised, 2),
        )

    @staticmethod
    def _by_percentage(income: float) -> dict[BudgetGroup, float]:
        planned = {
            group: round(income * percent / 100, 2)
            for group, percent in DEFAULT_PERCENTAGES.items()
        }
        largest = max(DEFAULT_PERCENTAGES, key=DEFAULT_PERCENTAGES.get)
        planned[largest] += round(income - sum(planned.values()), 2)
        return planned
