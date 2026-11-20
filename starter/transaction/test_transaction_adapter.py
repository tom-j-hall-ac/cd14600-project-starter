import unittest

from transaction.external_income_transaction import ExternalFreelanceIncome
from transaction.transaction import Transaction
from transaction.transaction_adapter import TransactionAdapter
from transaction.transaction_category import TransactionCategory


class TestTransactionAdapter(unittest.TestCase):

    def test_adapter_converts_freelance_income(self):
        external = ExternalFreelanceIncome(
            500, "INV-12345", "Website development")
        adapter = TransactionAdapter(external)
        transaction = adapter.to_transaction()
        self.assertEqual(
            transaction,
            Transaction(
                500, "INV-12345", "Website development",
                TransactionCategory.INCOME,
            ),
        )


if __name__ == "__main__":
    unittest.main()
