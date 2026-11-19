"""Defines the Import command."""

from balance.balance import Balance
from command.command import Command
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction_adapter import TransactionAdapter


class Import(Command):
    """Imports an external income transaction and applies it to the balance."""

    def __init__(self, balance: Balance, external: ExternalFreelanceIncome):
        self.balance = balance
        self.transaction = TransactionAdapter(external).to_transaction()

    def execute(self):
        self.balance.apply_transaction(self.transaction)

    def undo(self):
        self.balance.unapply_transaction(self.transaction)
