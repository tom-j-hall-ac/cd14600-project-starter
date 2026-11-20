"""This module serves as the entry point for the program."""

from balance.balance import Balance
from balance.balance_ledger_observer import BalanceLedgerObserver
from balance.balance_observer import LowBalanceAlertObserver, PrintObserver
from budget.budget_planner import BudgetPlanner
from budget.budget_processor import BudgetProcessor
from budget.fifty_thirty_twenty_strategy import FiftyThirtyTwentyStrategy
from budget.zero_based_strategy import ZeroBasedStrategy
from command.apply import Apply
from command.import_command import Import
from command.unapply import Unapply
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_processor import TransactionProcessor

LOW_BALANCE_THRESHOLD = 50


def income(amount, reference, detail):
    """Create an income transaction."""
    return Transaction(amount, reference, detail, TransactionCategory.INCOME)


def expense(amount, reference, detail):
    """Create an expense transaction."""
    return Transaction(amount, reference, detail, TransactionCategory.EXPENSE)


def warn_low_balance(alert):
    """Print a warning as soon as the balance drops below the threshold."""
    print(
        f"  WARNING: balance ${alert.balance.get_balance():.2f} is below "
        f"the {LOW_BALANCE_THRESHOLD} alert threshold."
    )


def announce_recovery(balance):
    """Print a message as soon as the balance is back above the threshold."""
    print(
        f"  Balance recovered: ${balance.get_balance():.2f} is back above "
        f"the {LOW_BALANCE_THRESHOLD} alert threshold."
    )


def register_observers(balance: Balance):
    """Subscribe the observers before any transaction is processed."""
    balance.register_observer(PrintObserver())
    balance.register_observer(BalanceLedgerObserver())
    balance.register_observer(
        LowBalanceAlertObserver(
            LOW_BALANCE_THRESHOLD,
            on_alert=warn_low_balance,
            on_recover=announce_recovery,
        )
    )


def process_transactions(balance: Balance):
    """Process a month of transactions through the TransactionProcessor.

    The emergency fund top-up drops the balance below the alert threshold,
    and the imported freelance income later brings it back above.
    """
    duplicate_payment = expense(90, "RCT-009", "Dining out (duplicate)")
    freelance_income = ExternalFreelanceIncome(
        1200, "INV-98765", "Mobile App Project"
    )
    processor = TransactionProcessor()
    processor.process_all([
        Apply(balance, income(4000, "PAY-001", "Salary")),
        Apply(balance, expense(1300, "RCT-001", "Monthly rent")),
        Apply(balance, expense(420, "RCT-002", "Groceries")),
        Apply(balance, expense(160, "RCT-003", "Electricity")),
        Apply(balance, expense(95, "RCT-004", "Dining out")),
        Apply(balance, expense(400, "RCT-005", "Weekend travel")),
        Apply(balance, expense(26, "RCT-006", "Streaming")),
        Apply(balance, expense(300, "RCT-007", "Pension")),
        Apply(balance, expense(1260, "RCT-008", "Emergency fund top-up")),
        Apply(balance, duplicate_payment),
        Unapply(balance, duplicate_payment),
        Import(balance, freelance_income),
        Apply(balance, expense(30, "RCT-006", "Car")),
        Apply(balance, expense(50, "RCT-006", "Plane")),
    ])


def print_budgets():
    """Print the ledger as a 50/30/20 budget and a zero-based budget."""
    summary = BudgetProcessor().process()
    planner = BudgetPlanner(FiftyThirtyTwentyStrategy())
    planner.print_plan(summary)
    print()
    planner.set_strategy(ZeroBasedStrategy())
    planner.print_plan(summary)


def main():
    print("Adding transactions...")

    balance = Balance.get_instance()
    register_observers(balance)
    process_transactions(balance)

    print()
    print_budgets()


if __name__ == "__main__":
    main()
