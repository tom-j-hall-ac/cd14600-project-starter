"""Defines the data produced by a budget strategy."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BudgetLine:
    """One line of a budget plan.

    Attributes:
        label: Name of the bucket or budget group.
        planned: Amount planned for the line.
        actual: Amount actually spent.
    """

    label: str
    planned: float
    actual: float

    @property
    def remaining(self) -> float:
        """The planned amount not yet spent (negative if overspent)."""
        return self.planned - self.actual


@dataclass(frozen=True)
class BudgetPlan:
    """A budget: how income is planned to be spent.

    Attributes:
        title: Name of the budget.
        income: The income being budgeted.
        lines: The planned lines of the budget.
        unallocated: Income not assigned to any line.
    """

    title: str
    income: float
    lines: tuple[BudgetLine, ...] = field(default_factory=tuple)
    unallocated: float = 0.0
