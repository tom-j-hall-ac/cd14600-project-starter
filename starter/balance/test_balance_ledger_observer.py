import unittest

from balance.balance import Balance
from balance.balance_ledger_observer import BalanceLedgerObserver
from command.apply import Apply
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_processor import TransactionProcessor
from ledger.ledger import Ledger


class TestBalanceLedgerObserver(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.balance.clear_observers()
        self.ledger = Ledger.get_instance()
        self.ledger.reset()
        self.balance.register_observer(BalanceLedgerObserver())
        self.income = Transaction(
            100, "PAY-1", "Salary", TransactionCategory.INCOME)
        self.expense = Transaction(
            30, "RCT-1", "Coffee", TransactionCategory.EXPENSE)

    def tearDown(self):
        self.balance.clear_observers()

    def test_uses_ledger_singleton_by_default(self):
        self.assertIs(BalanceLedgerObserver().ledger, self.ledger)

    def test_applied_transactions_are_recorded(self):
        self.balance.apply_transaction(self.income)
        self.balance.apply_transaction(self.expense)
        self.assertEqual(
            [(e.transaction, e.reversal) for e in self.ledger.entries],
            [(self.income, False), (self.expense, False)])

    def test_unapplied_transaction_is_recorded_as_reversal(self):
        self.balance.apply_transaction(self.expense)
        self.balance.unapply_transaction(self.expense)
        self.assertEqual(
            [e.reversal for e in self.ledger.entries], [False, True])

    def test_records_transactions_processed_through_commands(self):
        processor = TransactionProcessor()
        processor.process(Apply(self.balance, self.income))
        processor.undo_last()
        self.assertEqual(len(self.ledger), 2)


if __name__ == "__main__":
    unittest.main()
