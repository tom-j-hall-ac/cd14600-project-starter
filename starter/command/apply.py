"""Defines the Apply command."""

from balance.balance import Balance
from command.command import Command
from transaction.transaction import Transaction


class Apply(Command):
    """Applies a transaction to the balance."""

    def __init__(self, balance: Balance, transaction: Transaction):
        self.balance = balance
        self.transaction = transaction

    def execute(self):
        self.balance.apply_transaction(self.transaction)

    def undo(self):
        self.balance.unapply_transaction(self.transaction)
