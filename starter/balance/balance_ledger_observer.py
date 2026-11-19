"""Observer that records balance transactions in the Ledger."""

from balance.balance_observer import BalanceObserver
from ledger.ledger import Ledger


class BalanceLedgerObserver(BalanceObserver):
    """Stores each transaction processed by the Balance in the Ledger."""

    def __init__(self, ledger: Ledger | None = None):
        self.ledger = ledger if ledger is not None else Ledger.get_instance()

    def update(self, balance, transaction, reversal=False):
        self.ledger.record(transaction, reversal)
