import unittest

from budget.budget_processor import BudgetProcessor
from ledger.ledger import Ledger
from transaction.budget_group import BudgetGroup
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

INCOME = TransactionCategory.INCOME
EXPENSE = TransactionCategory.EXPENSE


class TestBudgetProcessor(unittest.TestCase):

    def setUp(self):
        self.ledger = Ledger.get_instance()
        self.ledger.reset()
        self.processor = BudgetProcessor(self.ledger)

    def tearDown(self):
        self.ledger.reset()

    def test_classify_matches_detail_keywords(self):
        cases = {
            "Monthly rent": BudgetGroup.HOUSING,
            "Weekly Groceries": BudgetGroup.GROCERIES,
            "Electricity bill": BudgetGroup.UTILITIES,
            "Credit card minimum": BudgetGroup.MINIMUM_DEBT_PAYMENTS,
            "Dining out": BudgetGroup.DINING_OUT,
            "Weekend travel": BudgetGroup.TRAVEL,
            "Climbing gym": BudgetGroup.HOBBIES,
            "Streaming service": BudgetGroup.SUBSCRIPTIONS,
            "Emergency transfer": BudgetGroup.EMERGENCY_FUNDS,
            "Pension contribution": BudgetGroup.RETIREMENT,
            "Extra loan payment": BudgetGroup.EXTRA_DEBT_PAYMENTS,
        }
        for detail, group in cases.items():
            t = Transaction(1, "REF", detail, EXPENSE)
            self.assertEqual(self.processor.classify(t), group, detail)

    def test_classify_unknown_detail(self):
        t = Transaction(1, "REF", "Mystery purchase", EXPENSE)
        self.assertIsNone(self.processor.classify(t))

    def test_process_applies_budget_group_to_transactions(self):
        t = Transaction(1200, "RENT-1", "Monthly rent", EXPENSE)
        self.ledger.record(t)
        self.processor.process()
        self.assertEqual(t.budget_group, BudgetGroup.HOUSING)

    def test_existing_budget_group_is_kept(self):
        t = Transaction(
            80, "REF", "Monthly rent", EXPENSE, BudgetGroup.HOBBIES)
        self.ledger.record(t)
        summary = self.processor.process()
        self.assertEqual(t.budget_group, BudgetGroup.HOBBIES)
        self.assertEqual(summary.spending[BudgetGroup.HOBBIES], 80)

    def test_income_is_totalled_and_has_no_group(self):
        t = Transaction(3000, "PAY-1", "Salary", INCOME)
        self.ledger.record(t)
        summary = self.processor.process()
        self.assertEqual(summary.income, 3000)
        self.assertIsNone(t.budget_group)

    def test_spending_is_totalled_per_group(self):
        self.ledger.record(Transaction(30, "R1", "Dining out", EXPENSE))
        self.ledger.record(Transaction(45, "R2", "Restaurant", EXPENSE))
        summary = self.processor.process()
        self.assertEqual(summary.spending[BudgetGroup.DINING_OUT], 75)

    def test_unmatched_spending_is_uncategorised(self):
        self.ledger.record(Transaction(25, "R1", "Mystery", EXPENSE))
        summary = self.processor.process()
        self.assertEqual(summary.uncategorised, 25)

    def test_reversals_are_subtracted(self):
        t = Transaction(50, "R1", "Groceries", EXPENSE)
        self.ledger.record(t)
        self.ledger.record(t, reversal=True)
        summary = self.processor.process()
        self.assertEqual(summary.spending[BudgetGroup.GROCERIES], 0)


if __name__ == "__main__":
    unittest.main()
