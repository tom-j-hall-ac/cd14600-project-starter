"""This module serves as the entry point for the program."""

from balance.balance import Balance
from balance.balance_ledger_observer import BalanceLedgerObserver
from balance.balance_observer import LowBalanceAlertObserver
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

INCOME = TransactionCategory.INCOME
EXPENSE = TransactionCategory.EXPENSE


def process_transactions(balance: Balance):
    """Process a month of transactions through the TransactionProcessor."""
    wrong_payment = Transaction(90, "RCT-009", "Dining out (duplicate)", EXPENSE)
    freelance_income = ExternalFreelanceIncome(
        1200, "INV-98765", "Mobile App Project"
    )
    processor = TransactionProcessor()
    processor.process_all([
        Apply(balance, Transaction(4000, "PAY-001", "Salary", INCOME)),
        Import(balance, freelance_income),
        Apply(balance, Transaction(1300, "RCT-001", "Monthly rent", EXPENSE)),
        Apply(balance, Transaction(420, "RCT-002", "Groceries", EXPENSE)),
        Apply(balance, Transaction(160, "RCT-003", "Electricity", EXPENSE)),
        Apply(balance, Transaction(95, "RCT-004", "Dining out", EXPENSE)),
        Apply(balance, Transaction(400, "RCT-005", "Weekend travel", EXPENSE)),
        Apply(balance, Transaction(26, "RCT-006", "Streaming", EXPENSE)),
        Apply(balance, Transaction(300, "RCT-007", "Pension", EXPENSE)),
        Apply(balance, wrong_payment),
        Unapply(balance, wrong_payment),
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
    balance.register_observer(BalanceLedgerObserver())
    low_balance_observer = LowBalanceAlertObserver(threshold=50)
    balance.register_observer(low_balance_observer)

    process_transactions(balance)
    print(balance.summary())
    if low_balance_observer.alert_triggered():
        print("Warning: balance is below the alert threshold.")

    print()
    print_budgets()


if __name__ == "__main__":
    main()
