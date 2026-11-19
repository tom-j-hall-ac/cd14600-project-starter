import unittest
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

class TestTransaction(unittest.TestCase):

    def test_transaction_creation(self):
        t = Transaction(100, "INV-12345", "Website development", TransactionCategory.EXPENSE)
        self.assertEqual(t.amount, 100)
        self.assertEqual(t.category, TransactionCategory.EXPENSE)

    def test_transaction_str(self):
        t = Transaction(50, "INV-1", "Consulting", TransactionCategory.INCOME)
        self.assertEqual(str(t), f"{TransactionCategory.INCOME}: 50 INV-1 Consulting")

    def test_transaction_equality(self):
        t1 = Transaction(20, "RCT-1", "Coffee", TransactionCategory.EXPENSE)
        t2 = Transaction(20, "RCT-1", "Coffee", TransactionCategory.EXPENSE)
        t3 = Transaction(30, "RCT-1", "Coffee", TransactionCategory.EXPENSE)
        self.assertEqual(t1, t2)
        self.assertNotEqual(t1, t3)

if __name__ == "__main__":
    unittest.main()
