"""Defines the Transaction class."""

from dataclasses import dataclass

from transaction.budget_group import BudgetGroup
from transaction.transaction_category import TransactionCategory


@dataclass
class Transaction:
    """Represents a financial transaction.

    Attributes:
        amount: The monetary value of the transaction.
        reference: A short reference identifying the transaction.
        detail: A free-text description of the transaction.
        category: The category the transaction belongs to.
        budget_group: The budget group the spending is allocated to, or
            None if it is not assigned to a group (e.g. income).
    """

    amount: float
    reference: str
    detail: str
    category: TransactionCategory
    budget_group: BudgetGroup | None = None

    def __str__(self) -> str:
        return f"{self.category}: {self.amount} {self.reference} {self.detail}"
