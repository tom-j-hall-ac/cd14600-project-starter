import unittest

from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

INCOME = TransactionCategory.INCOME
EXPENSE = TransactionCategory.EXPENSE


class TestTransaction(unittest.TestCase):

    def test_transaction_creation(self):
        transaction = Transaction(
            100, "INV-12345", "Website development", EXPENSE)
        self.assertEqual(transaction.amount, 100)
        self.assertEqual(transaction.category, EXPENSE)

    def test_transaction_str(self):
        transaction = Transaction(50, "INV-1", "Consulting", INCOME)
        self.assertEqual(
            str(transaction), f"{INCOME}: 50 INV-1 Consulting")

    def test_transaction_equality(self):
        coffee1 = Transaction(20, "RCT-1", "Coffee", EXPENSE)
        coffee2 = Transaction(20, "RCT-1", "Coffee", EXPENSE)
        dearer_coffee = Transaction(30, "RCT-1", "Coffee", EXPENSE)
        self.assertEqual(coffee1, coffee2)
        self.assertNotEqual(coffee1, dearer_coffee)


if __name__ == "__main__":
    unittest.main()
