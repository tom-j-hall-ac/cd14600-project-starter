import unittest

from balance.balance import Balance
from pattern.observer import Observer
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class RecordingObserver(Observer):
    """Test observer that remembers every update it receives."""

    def __init__(self):
        self.updates = []

    def update(self, *args, **kwargs):
        self.updates.append(args)


class TestBalance(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.balance.clear_observers()

    def tearDown(self):
        self.balance.clear_observers()

    def test_initial_balance(self):
        self.assertEqual(self.balance.get_balance(), 0.0)

    def test_accessor_calls_return_same_instance(self):
        balance1 = Balance.get_instance()
        balance2 = Balance.get_instance()
        self.assertIs(balance1, balance2)

    def test_direct_construction_returns_accessor_instance(self):
        self.assertIs(Balance(), Balance.get_instance())

    def test_repeated_direct_construction_returns_same_instance(self):
        self.assertIs(Balance(), Balance())

    def test_repeated_construction_keeps_balance(self):
        self.balance.add_income(100)
        Balance()
        Balance.get_instance()
        self.assertEqual(self.balance.get_balance(), 100)
        self.assertEqual(Balance().get_balance(), 100)

    def test_repeated_construction_keeps_observers(self):
        observer = RecordingObserver()
        self.balance.register_observer(observer)
        Balance()
        self.balance.add_income(10)
        income = Transaction(
            10, "INV-1", "Tip", TransactionCategory.INCOME)
        Balance().apply_transaction(income)
        self.assertEqual(len(observer.updates), 1)

    def test_add_income(self):
        self.balance.add_income(100)
        self.assertEqual(self.balance.get_balance(), 100)

    def test_add_expense(self):
        self.balance.add_expense(40)
        self.assertEqual(self.balance.get_balance(), -40)

    def test_apply_transaction_income(self):
        income = Transaction(
            150, "INV-12345", "Website development",
            TransactionCategory.INCOME)
        self.balance.apply_transaction(income)
        self.assertEqual(self.balance.get_balance(), 150)

    def test_apply_transaction_expense(self):
        expense = Transaction(
            60, "RCT-12345", "Coffee", TransactionCategory.EXPENSE)
        self.balance.apply_transaction(expense)
        self.assertEqual(self.balance.get_balance(), -60)

    def test_unapply_transaction_reverses_apply(self):
        expense = Transaction(
            60, "RCT-12345", "Coffee", TransactionCategory.EXPENSE)
        self.balance.apply_transaction(expense)
        self.balance.unapply_transaction(expense)
        self.assertEqual(self.balance.get_balance(), 0)

    def test_summary(self):
        self.balance.add_income(100)
        self.balance.add_expense(40)
        self.assertEqual(
            " ".join(self.balance.summary().split()), "Net balance: $ 60.00")

    # There is no invalid-category test: TransactionCategory is an enum,
    # so the type is already constrained.

    def test_reset(self):
        self.balance.add_income(100)
        self.balance.add_expense(50)
        self.balance.reset()
        self.assertEqual(self.balance.get_balance(), 0.0)


if __name__ == "__main__":
    unittest.main()
