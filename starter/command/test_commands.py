import unittest

from balance.balance import Balance
from command.apply import Apply
from command.command import Command
from command.import_command import Import
from command.unapply import Unapply
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory


class TestCommands(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.income = Transaction(
            100, "PAY-1", "Salary", TransactionCategory.INCOME)
        self.expense = Transaction(
            40, "RCT-1", "Groceries", TransactionCategory.EXPENSE)

    def test_commands_extend_command(self):
        for cls in (Apply, Unapply, Import):
            self.assertTrue(issubclass(cls, Command))

    def test_apply_income_and_undo(self):
        command = Apply(self.balance, self.income)
        command.execute()
        self.assertEqual(self.balance.get_balance(), 100)
        command.undo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_apply_expense_and_undo(self):
        command = Apply(self.balance, self.expense)
        command.execute()
        self.assertEqual(self.balance.get_balance(), -40)
        command.undo()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_unapply_reverses_applied_transaction(self):
        self.balance.apply_transaction(self.expense)
        command = Unapply(self.balance, self.expense)
        command.execute()
        self.assertEqual(self.balance.get_balance(), 0)
        command.undo()
        self.assertEqual(self.balance.get_balance(), -40)

    def test_import_applies_external_income_and_undo(self):
        external = ExternalFreelanceIncome(500, "INV-1", "Website")
        command = Import(self.balance, external)
        command.execute()
        self.assertEqual(self.balance.get_balance(), 500)
        command.undo()
        self.assertEqual(self.balance.get_balance(), 0)


if __name__ == "__main__":
    unittest.main()
