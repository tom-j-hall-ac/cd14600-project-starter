"""Defines the Balance singleton that tracks the net balance."""

from pattern.observer import ObserverSubject
from pattern.singleton import Singleton
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class Balance(Singleton, ObserverSubject):
    """Singleton that tracks the net balance and notifies observers."""

    def __init__(self):
        super().__init__()
        self._balance = 0.0

    def reset(self):
        """Reset the balance to zero."""
        self._balance = 0.0

    def add_income(self, amount):
        """Add income to the balance."""
        self._balance += amount

    def add_expense(self, amount):
        """Subtract expense from the balance."""
        self._balance -= amount

    def apply_transaction(self, transaction: Transaction):
        """Apply a Transaction to the balance, then notify observers.

        Args:
            transaction: The transaction to apply.
        """
        if transaction.category == TransactionCategory.INCOME:
            self.add_income(transaction.amount)
        else:
            self.add_expense(transaction.amount)
        self.notify(self, transaction)

    def get_balance(self):
        """Get the current net balance."""
        return self._balance

    def summary(self):
        """Return a summary string of the net balance."""
        return f"Net balance: {self.get_balance():.2f}"
