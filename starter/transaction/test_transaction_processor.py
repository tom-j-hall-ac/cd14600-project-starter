import unittest

from balance.balance import Balance
from command.apply import Apply
from command.import_command import Import
from command.unapply import Unapply
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_processor import TransactionProcessor


class TestTransactionProcessor(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.processor = TransactionProcessor()
        self.income = Transaction(
            100, "PAY-1", "Salary", TransactionCategory.INCOME)
        self.expense = Transaction(
            30, "RCT-1", "Coffee", TransactionCategory.EXPENSE)

    def test_process_executes_and_records_command(self):
        command = Apply(self.balance, self.income)
        self.processor.process(command)
        self.assertEqual(self.balance.get_balance(), 100)
        self.assertEqual(self.processor.history, (command,))

    def test_process_all_runs_commands_in_order(self):
        external = ExternalFreelanceIncome(500, "INV-1", "Website")
        self.processor.process_all([
            Apply(self.balance, self.income),
            Apply(self.balance, self.expense),
            Import(self.balance, external),
            Unapply(self.balance, self.expense),
        ])
        self.assertEqual(self.balance.get_balance(), 600)
        self.assertEqual(len(self.processor.history), 4)

    def test_undo_last_reverses_most_recent_command(self):
        self.processor.process(Apply(self.balance, self.income))
        self.processor.process(Apply(self.balance, self.expense))
        self.assertTrue(self.processor.undo_last())
        self.assertEqual(self.balance.get_balance(), 100)
        self.assertEqual(len(self.processor.history), 1)

    def test_undo_last_with_empty_history(self):
        self.assertFalse(self.processor.undo_last())


if __name__ == "__main__":
    unittest.main()
