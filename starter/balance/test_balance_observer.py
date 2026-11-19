import unittest
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver

class TestLowBalanceAlertObserver(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_alert_triggers_on_low_balance(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.balance.apply_transaction(Transaction(100, "INV-101","Web scripting analysis", TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered())

        self.balance.apply_transaction(Transaction(60, "INV-102","Webscript design", TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered())

        self.balance.apply_transaction(Transaction(100, "INV-102","Webscript development", TransactionCategory.INCOME))
        self.assertFalse(observer.alert_triggered())

        self.balance.apply_transaction(Transaction(60, "RCT-101", "Travel", TransactionCategory.EXPENSE))
        self.assertFalse(observer.alert_triggered())
        
        self.balance.apply_transaction(Transaction(60, "RCT-102", "Accommodation", TransactionCategory.EXPENSE))
        self.assertTrue(observer.alert_triggered())

if __name__ == "__main__":
    unittest.main()
