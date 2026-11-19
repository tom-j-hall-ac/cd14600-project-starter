"""This module serves as the entry point for the program."""

from balance.balance import Balance
from balance.balance_observer import LowBalanceAlertObserver, PrintObserver
from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction import Transaction
from transaction.transaction_adapter import TransactionAdapter
from transaction.transaction_category import TransactionCategory


def main():
    print("Adding transactions...")

    balance = Balance.get_instance()
    balance.register_observer(PrintObserver())
    low_balance_observer = LowBalanceAlertObserver(threshold=50)
    balance.register_observer(low_balance_observer)

    # Create standard transactions
    income = TransactionCategory.INCOME
    expense = TransactionCategory.EXPENSE
    transactions = [
        Transaction(100, "PAY-001", "Salary", income),
        Transaction(50, "RCT-001", "Groceries", expense),
        Transaction(200, "PAY-002", "Bonus", income),
        Transaction(75, "RCT-002", "Dining out", expense),
    ]

    # Create an external income transaction (via Adapter pattern)
    freelance_income = ExternalFreelanceIncome(
        1200, "INV-98765", "Mobile App Project"
    )
    adapted_transaction = TransactionAdapter(freelance_income).to_transaction()

    for transaction in transactions + [adapted_transaction]:
        balance.apply_transaction(transaction)

    if low_balance_observer.alert_triggered():
        print("Warning: balance is below the alert threshold.")


if __name__ == "__main__":
    main()
