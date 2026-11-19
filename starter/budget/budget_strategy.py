"""Defines the abstract strategy used by the BudgetPlanner."""

from abc import ABC, abstractmethod

from budget.budget_plan import BudgetPlan
from budget.budget_summary import BudgetSummary


class BudgetStrategy(ABC):
    """Strategy interface: a way of turning income into a budget plan."""

    @abstractmethod
    def create_plan(self, summary: BudgetSummary) -> BudgetPlan:
        """Create a budget plan from the income and spending in a summary."""
