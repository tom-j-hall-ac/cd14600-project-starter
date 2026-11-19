"""Defines the BudgetProcessor that applies budget groups to the ledger."""

from budget.budget_summary import BudgetSummary
from ledger.ledger import Ledger
from transaction.budget_group import BudgetGroup
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

# Keywords matched (case-insensitively) against a transaction's detail.
# The first matching rule wins.
DEFAULT_RULES: tuple[tuple[str, BudgetGroup], ...] = (
    ("rent", BudgetGroup.HOUSING),
    ("mortgage", BudgetGroup.HOUSING),
    ("grocer", BudgetGroup.GROCERIES),
    ("supermarket", BudgetGroup.GROCERIES),
    ("electric", BudgetGroup.UTILITIES),
    ("water", BudgetGroup.UTILITIES),
    ("internet", BudgetGroup.UTILITIES),
    ("minimum", BudgetGroup.MINIMUM_DEBT_PAYMENTS),
    ("extra", BudgetGroup.EXTRA_DEBT_PAYMENTS),
    ("dining", BudgetGroup.DINING_OUT),
    ("restaurant", BudgetGroup.DINING_OUT),
    ("travel", BudgetGroup.TRAVEL),
    ("hobby", BudgetGroup.HOBBIES),
    ("gym", BudgetGroup.HOBBIES),
    ("subscription", BudgetGroup.SUBSCRIPTIONS),
    ("streaming", BudgetGroup.SUBSCRIPTIONS),
    ("emergency", BudgetGroup.EMERGENCY_FUNDS),
    ("pension", BudgetGroup.RETIREMENT),
    ("retirement", BudgetGroup.RETIREMENT),
)


class BudgetProcessor:
    """Applies a budget group to every ledger transaction and totals them."""

    def __init__(self, ledger: Ledger | None = None, rules=DEFAULT_RULES):
        self.ledger = ledger if ledger is not None else Ledger.get_instance()
        self.rules = rules

    def classify(self, transaction: Transaction) -> BudgetGroup | None:
        """Return the budget group matching a transaction's detail, if any."""
        detail = transaction.detail.lower()
        for keyword, group in self.rules:
            if keyword in detail:
                return group
        return None

    def process(self) -> BudgetSummary:
        """Assign budget groups to ledger expenses and total everything.

        Expenses that already have a budget group keep it. Reversed entries
        are subtracted from the totals.
        """
        summary = BudgetSummary()
        for entry in self.ledger.entries:
            transaction = entry.transaction
            sign = -1 if entry.reversal else 1
            if transaction.category == TransactionCategory.INCOME:
                summary.income += sign * transaction.amount
                continue
            if transaction.budget_group is None:
                transaction.budget_group = self.classify(transaction)
            if transaction.budget_group is None:
                summary.uncategorised += sign * transaction.amount
            else:
                summary.spending[transaction.budget_group] += (
                    sign * transaction.amount
                )
        return summary
