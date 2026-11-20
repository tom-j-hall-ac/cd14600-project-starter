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
        self._adjust(transaction, sign=1)

    def unapply_transaction(self, transaction: Transaction):
        """Reverse a previously applied Transaction, then notify observers.

        Args:
            transaction: The transaction to reverse.
        """
        self._adjust(transaction, sign=-1)

    def _adjust(self, transaction: Transaction, sign: int):
        """Apply (sign=1) or reverse (sign=-1) a transaction."""
        if transaction.category == TransactionCategory.INCOME:
            self._balance += sign * transaction.amount
        else:
            self._balance -= sign * transaction.amount
        self.notify(self, transaction, reversal=sign < 0)

    def get_balance(self):
        """Get the current net balance."""
        return self._balance

    def summary(self):
        """Return a summary string of the net balance."""
        return f"Net balance: ${self.get_balance():>9.2f}"
