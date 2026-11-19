"""Defines the Unapply command."""

from balance.balance import Balance
from command.command import Command
from transaction.transaction import Transaction


class Unapply(Command):
    """Reverses a previously applied transaction on the balance."""

    def __init__(self, balance: Balance, transaction: Transaction):
        self.balance = balance
        self.transaction = transaction

    def execute(self):
        self.balance.unapply_transaction(self.transaction)

    def undo(self):
        self.balance.apply_transaction(self.transaction)
