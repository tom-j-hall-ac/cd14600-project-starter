import contextlib
import io
import unittest

from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver, PrintObserver
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

INCOME = TransactionCategory.INCOME
EXPENSE = TransactionCategory.EXPENSE


class BalanceObserverTestCase(unittest.TestCase):
    """Gives each test a clean Balance with no observers."""

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.balance.clear_observers()

    def tearDown(self):
        self.balance.clear_observers()

    def pay(self, amount, detail="Payment"):
        self.balance.apply_transaction(
            Transaction(amount, "REF", detail, INCOME))

    def spend(self, amount, detail="Purchase"):
        self.balance.apply_transaction(
            Transaction(amount, "REF", detail, EXPENSE))


class TestLowBalanceAlertObserver(BalanceObserverTestCase):

    def test_alert_triggers_on_low_balance(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.pay(100, "Web scripting analysis")
        self.assertFalse(observer.alert_triggered())

        self.spend(60, "Webscript design")
        self.assertTrue(observer.alert_triggered())

        self.pay(100, "Webscript development")
        self.assertFalse(observer.alert_triggered())

        self.spend(60, "Travel")
        self.assertFalse(observer.alert_triggered())

        self.spend(60, "Accommodation")
        self.assertTrue(observer.alert_triggered())

    def test_no_alert_when_balance_equals_threshold(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.pay(100)
        self.spend(50)

        self.assertEqual(self.balance.get_balance(), 50)
        self.assertFalse(observer.alert_triggered())

    def test_alert_when_balance_is_just_below_threshold(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.pay(100)
        self.spend(50.01)

        self.assertTrue(observer.alert_triggered())

    def test_alert_records_triggering_transaction(self):
        observer = LowBalanceAlertObserver(threshold=50)
        self.balance.register_observer(observer)

        self.pay(100)
        self.spend(60, "Rent")

        alert = observer.low_balance_alert
        self.assertIs(alert.balance, self.balance)
        self.assertEqual(alert.transaction.detail, "Rent")

    def test_on_alert_called_when_balance_drops_below_threshold(self):
        events = []
        observer = LowBalanceAlertObserver(
            threshold=50,
            on_alert=lambda alert: events.append(
                ("alert", self.balance.get_balance())),
            on_recover=lambda balance: events.append(
                ("recover", balance.get_balance())),
        )
        self.balance.register_observer(observer)

        self.pay(100)
        self.assertEqual(events, [])

        self.spend(60)
        self.assertEqual(events, [("alert", 40)])

    def test_on_recover_called_when_balance_returns_above_threshold(self):
        events = []
        observer = LowBalanceAlertObserver(
            threshold=50,
            on_alert=lambda alert: events.append("alert"),
            on_recover=lambda balance: events.append("recover"),
        )
        self.balance.register_observer(observer)

        self.pay(100)
        self.spend(60)
        self.pay(100)

        self.assertEqual(events, ["alert", "recover"])

    def test_callbacks_fire_once_per_dip(self):
        events = []
        observer = LowBalanceAlertObserver(
            threshold=50,
            on_alert=lambda alert: events.append("alert"),
            on_recover=lambda balance: events.append("recover"),
        )
        self.balance.register_observer(observer)

        self.pay(100)
        self.spend(60)
        self.spend(10)
        self.pay(100)
        self.pay(10)

        self.assertEqual(events, ["alert", "recover"])

    def test_recovering_to_exactly_threshold_counts_as_recovered(self):
        events = []
        observer = LowBalanceAlertObserver(
            threshold=50,
            on_recover=lambda balance: events.append(balance.get_balance()),
        )
        self.balance.register_observer(observer)

        self.pay(40)
        self.pay(10)

        self.assertEqual(events, [50])


class TestPrintObserver(BalanceObserverTestCase):

    def capture_output(self, action):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            action()
        # Collapse the column padding so tests do not depend on widths.
        return [" ".join(line.split())
                for line in output.getvalue().splitlines()]

    def test_prints_balance_after_each_transaction(self):
        self.balance.register_observer(PrintObserver())

        def process():
            self.pay(100, "Salary")
            self.spend(30, "Coffee")

        lines = self.capture_output(process)

        self.assertEqual(lines, [
            "Applied INCOME $ 100.00 Salary Net balance: $ 100.00",
            "Applied EXPENSE $ 30.00 Coffee Net balance: $ 70.00",
        ])

    def test_prints_reversals(self):
        self.balance.register_observer(PrintObserver())
        coffee = Transaction(30, "RCT-1", "Coffee", EXPENSE)

        def process():
            self.balance.apply_transaction(coffee)
            self.balance.unapply_transaction(coffee)

        lines = self.capture_output(process)

        self.assertEqual(lines, [
            "Applied EXPENSE $ 30.00 Coffee Net balance: $ -30.00",
            "Reversed EXPENSE $ 30.00 Coffee Net balance: $ 0.00",
        ])

    def test_prints_nothing_when_not_registered(self):
        lines = self.capture_output(lambda: self.pay(100))
        self.assertEqual(lines, [])


if __name__ == "__main__":
    unittest.main()
