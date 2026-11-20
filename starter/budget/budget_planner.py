"""Defines the BudgetPlanner, the context of the Strategy pattern."""

from budget.budget_plan import BudgetPlan
from budget.budget_strategy import BudgetStrategy
from budget.budget_summary import BudgetSummary


class BudgetPlanner:
    """Creates and prints budgets using a swappable BudgetStrategy."""

    def __init__(self, strategy: BudgetStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: BudgetStrategy):
        """Change the strategy used to create budgets."""
        self.strategy = strategy

    def create_plan(self, summary: BudgetSummary) -> BudgetPlan:
        """Create a budget plan using the current strategy."""
        return self.strategy.create_plan(summary)

    def render(self, summary: BudgetSummary) -> str:
        """Return the budget for the summary as printable text."""
        plan = self.create_plan(summary)
        rows = [
            plan.title,
            f"Income: {plan.income:.2f}",
            f"{'':<28}{'Planned':>10}{'Actual':>10}{'Remaining':>11}",
        ]
        rows += [
            f"{line.label:<28}{line.planned:>10.2f}"
            f"{line.actual:>10.2f}{line.remaining:>11.2f}"
            for line in plan.lines
        ]
        rows.append(f"Unallocated: {plan.unallocated:.2f}")
        rows.append(f"Uncategorised spending: {plan.uncategorised:.2f}")
        return "\n".join(rows)

    def print_plan(self, summary: BudgetSummary):
        """Print the budget for the summary."""
        print(self.render(summary))
