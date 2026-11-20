import contextlib
import io
import unittest

import main
from balance.balance import Balance
from ledger.ledger import Ledger


class TestMain(unittest.TestCase):

    def setUp(self):
        self.reset_shared_state()

    def tearDown(self):
        self.reset_shared_state()

    @staticmethod
    def reset_shared_state():
        balance = Balance.get_instance()
        balance.reset()
        balance.clear_observers()
        Ledger.get_instance().reset()

    @staticmethod
    def run_main():
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            main.main()
        return output.getvalue().splitlines()

    @staticmethod
    def index_of(lines, text):
        return next(i for i, line in enumerate(lines) if text in line)

    def test_prints_balance_after_every_transaction(self):
        lines = self.run_main()
        updates = [line for line in lines
                   if line.startswith(("Applied", "Reversed"))]
        self.assertEqual(len(updates), len(Ledger.get_instance()))
        self.assertTrue(all("Net balance:" in line for line in updates))

    def test_warns_once_at_the_moment_balance_drops_below_threshold(self):
        lines = self.run_main()
        warnings = [line for line in lines if "WARNING" in line]
        self.assertEqual(len(warnings), 1)

        top_up = self.index_of(lines, "Emergency fund top-up")
        warning = self.index_of(lines, "WARNING")
        next_transaction = self.index_of(lines, "Dining out (duplicate)")
        self.assertEqual(warning, top_up + 1)
        self.assertLess(warning, next_transaction)
        self.assertIn("39.00", lines[top_up])

    def test_announces_recovery_after_the_dip(self):
        lines = self.run_main()
        warning = self.index_of(lines, "WARNING")
        income = self.index_of(lines, "Mobile App Project")
        recovery = self.index_of(lines, "Balance recovered")
        self.assertLess(warning, income)
        self.assertEqual(recovery, income + 1)
        self.assertIn("1239.00", lines[income])

    def test_budgets_are_printed_after_processing(self):
        lines = self.run_main()
        recovery = self.index_of(lines, "Balance recovered")
        self.assertLess(recovery, self.index_of(lines, "50/30/20 Budget"))
        self.assertLess(recovery, self.index_of(lines, "Zero-Based Budget"))

    def test_every_transaction_is_stored_in_the_ledger(self):
        lines = self.run_main()
        updates = [line for line in lines
                   if line.startswith(("Applied", "Reversed"))]
        self.assertGreater(len(updates), 0)
        self.assertEqual(len(Ledger.get_instance()), len(updates))

    def test_both_budgets_show_uncategorised_spending(self):
        lines = self.run_main()
        uncategorised = [line for line in lines
                         if line.startswith("Uncategorised spending")]
        self.assertEqual(
            uncategorised, ["Uncategorised spending: 80.00"] * 2)


if __name__ == "__main__":
    unittest.main()
