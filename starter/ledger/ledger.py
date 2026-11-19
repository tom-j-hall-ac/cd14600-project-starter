"""Defines the Ledger singleton that stores processed transactions."""

from dataclasses import dataclass

from pattern.singleton import Singleton
from transaction.transaction import Transaction


@dataclass(frozen=True)
class LedgerEntry:
    """A transaction as processed by the balance.

    Attributes:
        transaction: The transaction that was processed.
        reversal: True if the transaction was unapplied, not applied.
    """

    transaction: Transaction
    reversal: bool = False


class Ledger(Singleton):
    """Singleton that stores processed transactions for later processing."""

    def __init__(self):
        self._entries: list[LedgerEntry] = []

    @property
    def entries(self) -> tuple[LedgerEntry, ...]:
        """The recorded entries, oldest first."""
        return tuple(self._entries)

    def record(self, transaction: Transaction, reversal: bool = False):
        """Store a processed transaction in the ledger."""
        self._entries.append(LedgerEntry(transaction, reversal))

    def reset(self):
        """Remove all entries from the ledger."""
        self._entries.clear()

    def __len__(self) -> int:
        return len(self._entries)
