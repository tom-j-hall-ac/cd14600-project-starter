import unittest

from ledger.ledger import Ledger
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TestLedger(unittest.TestCase):

    def setUp(self):
        self.ledger = Ledger.get_instance()
        self.ledger.reset()
        self.transaction = Transaction(
            100, "PAY-1", "Salary", TransactionCategory.INCOME)

    def test_singleton_instance(self):
        self.assertIs(Ledger.get_instance(), Ledger.get_instance())

    def test_starts_empty(self):
        self.assertEqual(len(self.ledger), 0)
        self.assertEqual(self.ledger.entries, ())

    def test_record_stores_entry(self):
        self.ledger.record(self.transaction)
        entry, = self.ledger.entries
        self.assertEqual(entry.transaction, self.transaction)
        self.assertFalse(entry.reversal)

    def test_record_reversal(self):
        self.ledger.record(self.transaction, reversal=True)
        self.assertTrue(self.ledger.entries[0].reversal)

    def test_entries_keep_order(self):
        other = Transaction(
            20, "RCT-1", "Coffee", TransactionCategory.EXPENSE)
        self.ledger.record(self.transaction)
        self.ledger.record(other)
        self.assertEqual(
            [e.transaction for e in self.ledger.entries],
            [self.transaction, other])

    def test_reset_clears_entries(self):
        self.ledger.record(self.transaction)
        self.ledger.reset()
        self.assertEqual(len(self.ledger), 0)


if __name__ == "__main__":
    unittest.main()
