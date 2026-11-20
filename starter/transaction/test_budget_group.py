import unittest
from collections import defaultdict

from balance.balance import Balance
from transaction.budget_group import BudgetGroup
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory

INCOME = TransactionCategory.INCOME
EXPENSE = TransactionCategory.EXPENSE

# Fictitious monthly spending, one entry per budget group.
FICTITIOUS_SPENDING = {
    BudgetGroup.HOUSING: (1200.00, "RENT-01", "Monthly rent"),
    BudgetGroup.GROCERIES: (350.50, "GRO-01", "Weekly shop"),
    BudgetGroup.UTILITIES: (180.25, "UTL-01", "Electricity and water"),
    BudgetGroup.MINIMUM_DEBT_PAYMENTS: (
        150.00, "DEBT-01", "Credit card minimum"),
    BudgetGroup.DINING_OUT: (95.00, "DIN-01", "Restaurant"),
    BudgetGroup.TRAVEL: (400.00, "TRV-01", "Weekend train trip"),
    BudgetGroup.HOBBIES: (60.00, "HOB-01", "Climbing gym"),
    BudgetGroup.SUBSCRIPTIONS: (25.99, "SUB-01", "Streaming service"),
    BudgetGroup.EMERGENCY_FUNDS: (200.00, "EMG-01", "Rainy day transfer"),
    BudgetGroup.RETIREMENT: (300.00, "RET-01", "Pension contribution"),
    BudgetGroup.EXTRA_DEBT_PAYMENTS: (250.00, "DEBT-02", "Extra loan payment"),
}


def make_spending():
    return [
        Transaction(amount, ref, detail, TransactionCategory.EXPENSE, group)
        for group, (amount, ref, detail) in FICTITIOUS_SPENDING.items()
    ]


class TestBudgetGroup(unittest.TestCase):

    def test_all_budget_groups_present(self):
        names = {g.name for g in BudgetGroup}
        self.assertEqual(names, {
            "HOUSING", "GROCERIES", "UTILITIES", "MINIMUM_DEBT_PAYMENTS",
            "DINING_OUT", "TRAVEL", "HOBBIES", "SUBSCRIPTIONS",
            "EMERGENCY_FUNDS", "RETIREMENT", "EXTRA_DEBT_PAYMENTS",
        })

    def test_transaction_holds_budget_group(self):
        transaction = Transaction(
            50, "REF", "Detail", EXPENSE, BudgetGroup.GROCERIES)
        self.assertEqual(transaction.budget_group, BudgetGroup.GROCERIES)

    def test_budget_group_defaults_to_none(self):
        transaction = Transaction(50, "REF", "Detail", INCOME)
        self.assertIsNone(transaction.budget_group)

    def test_budget_group_affects_equality(self):
        trip1 = Transaction(10, "REF", "Detail", EXPENSE, BudgetGroup.TRAVEL)
        trip2 = Transaction(10, "REF", "Detail", EXPENSE, BudgetGroup.TRAVEL)
        hobby = Transaction(10, "REF", "Detail", EXPENSE, BudgetGroup.HOBBIES)
        self.assertEqual(trip1, trip2)
        self.assertNotEqual(trip1, hobby)


class TestFictitiousSpending(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()

    def test_spending_covers_every_budget_group(self):
        groups = {t.budget_group for t in make_spending()}
        self.assertEqual(groups, set(BudgetGroup))

    def test_total_spending_reduces_balance(self):
        self.balance.apply_transaction(
            Transaction(5000, "PAY-01", "Salary", TransactionCategory.INCOME)
        )
        for t in make_spending():
            self.balance.apply_transaction(t)

        total = sum(amount for amount, _, _ in FICTITIOUS_SPENDING.values())
        self.assertAlmostEqual(self.balance.get_balance(), 5000 - total)

    def test_spending_totals_per_group(self):
        totals = defaultdict(float)
        for t in make_spending():
            totals[t.budget_group] += t.amount

        for group, (amount, _, _) in FICTITIOUS_SPENDING.items():
            self.assertAlmostEqual(totals[group], amount)


if __name__ == "__main__":
    unittest.main()
