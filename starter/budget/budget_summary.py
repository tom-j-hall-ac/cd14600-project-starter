"""Defines the BudgetSummary produced by the BudgetProcessor."""

from dataclasses import dataclass, field

from transaction.budget_group import BudgetGroup


@dataclass
class BudgetSummary:
    """Income and spending totals taken from the ledger.

    Attributes:
        income: Net income received.
        spending: Net amount spent in each budget group.
        uncategorised: Net spending that matched no budget group.
    """

    income: float = 0.0
    spending: dict[BudgetGroup, float] = field(
        default_factory=lambda: {group: 0.0 for group in BudgetGroup}
    )
    uncategorised: float = 0.0

    def spent_in(self, groups) -> float:
        """Return the total spent across the given budget groups."""
        return sum(self.spending[group] for group in groups)
