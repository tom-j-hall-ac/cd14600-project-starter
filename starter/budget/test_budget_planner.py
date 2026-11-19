import unittest

from budget.budget_planner import BudgetPlanner
from budget.budget_strategy import BudgetStrategy
from budget.budget_summary import BudgetSummary
from budget.fifty_thirty_twenty_strategy import FiftyThirtyTwentyStrategy
from budget.zero_based_strategy import ZeroBasedStrategy
from transaction.budget_group import BudgetGroup


def make_summary(income=5000.0):
    summary = BudgetSummary(income=income)
    summary.spending[BudgetGroup.HOUSING] = 1200
    summary.spending[BudgetGroup.GROCERIES] = 300
    summary.spending[BudgetGroup.DINING_OUT] = 100
    summary.spending[BudgetGroup.RETIREMENT] = 400
    return summary


class TestFiftyThirtyTwentyStrategy(unittest.TestCase):

    def test_splits_income_50_30_20(self):
        plan = FiftyThirtyTwentyStrategy().create_plan(make_summary())
        self.assertEqual(
            [line.planned for line in plan.lines], [2500, 1500, 1000])
        self.assertEqual(plan.unallocated, 0)

    def test_actuals_are_summed_per_bucket(self):
        plan = FiftyThirtyTwentyStrategy().create_plan(make_summary())
        self.assertEqual(
            [line.actual for line in plan.lines], [1500, 100, 400])
        self.assertEqual(plan.lines[0].remaining, 1000)


class TestZeroBasedStrategy(unittest.TestCase):

    def test_every_dollar_is_allocated_by_default(self):
        plan = ZeroBasedStrategy().create_plan(make_summary(3333.33))
        self.assertEqual(len(plan.lines), len(BudgetGroup))
        self.assertAlmostEqual(sum(l.planned for l in plan.lines), 3333.33)
        self.assertEqual(plan.unallocated, 0)

    def test_actuals_come_from_summary(self):
        plan = ZeroBasedStrategy().create_plan(make_summary())
        housing = plan.lines[0]
        self.assertEqual(housing.label, "Housing")
        self.assertEqual(housing.actual, 1200)

    def test_explicit_allocations_report_unallocated(self):
        strategy = ZeroBasedStrategy({
            BudgetGroup.HOUSING: 2000,
            BudgetGroup.GROCERIES: 500,
        })
        plan = strategy.create_plan(make_summary())
        self.assertEqual(plan.unallocated, 2500)
        self.assertEqual(plan.lines[0].planned, 2000)
        self.assertEqual(plan.lines[4].planned, 0)


class TestBudgetPlanner(unittest.TestCase):

    def test_strategies_extend_budget_strategy(self):
        self.assertTrue(issubclass(FiftyThirtyTwentyStrategy, BudgetStrategy))
        self.assertTrue(issubclass(ZeroBasedStrategy, BudgetStrategy))

    def test_planner_uses_current_strategy(self):
        planner = BudgetPlanner(FiftyThirtyTwentyStrategy())
        self.assertEqual(
            planner.create_plan(make_summary()).title, "50/30/20 Budget")
        planner.set_strategy(ZeroBasedStrategy())
        self.assertEqual(
            planner.create_plan(make_summary()).title, "Zero-Based Budget")

    def test_render_contains_title_lines_and_unallocated(self):
        text = BudgetPlanner(FiftyThirtyTwentyStrategy()).render(
            make_summary())
        self.assertIn("50/30/20 Budget", text)
        self.assertIn("Needs (50%)", text)
        self.assertIn("2500.00", text)
        self.assertIn("Unallocated: 0.00", text)


if __name__ == "__main__":
    unittest.main()
