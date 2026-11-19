"""Adapts external transaction formats to the standard Transaction."""

from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TransactionAdapter:
    """Adapts an ExternalFreelanceIncome to a Transaction."""

    def __init__(self, external_transaction: ExternalFreelanceIncome):
        self.external_transaction = external_transaction

    def to_transaction(self):
        """Convert an external transaction to a standard Transaction."""
        external = self.external_transaction
        return Transaction(
            external.amount,
            external.invoice_id,
            external.description,
            TransactionCategory.INCOME,
        )
