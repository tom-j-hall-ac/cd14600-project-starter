"""Observers that react to changes in the Balance."""

from __future__ import annotations

from abc import abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pattern.observer import Observer
from transaction.transaction import Transaction

if TYPE_CHECKING:
    from balance.balance import Balance


class BalanceObserver(Observer):
    """Interface for objects that want to be told about balance updates."""

    @abstractmethod
    def update(
        self,
        balance: Balance,
        transaction: Transaction,
        reversal: bool = False,
    ):
        """Handle a balance update caused by a transaction.

        Args:
            balance: The balance that changed.
            transaction: The transaction that was processed.
            reversal: True if the transaction was unapplied.
        """


class PrintObserver(BalanceObserver):
    """Prints the balance after every transaction."""

    def update(
        self,
        balance: Balance,
        transaction: Transaction,
        reversal: bool = False,
    ):
        action = "Reversed" if reversal else "Applied"
        print(
            f"{action:<10} "
            f"{transaction.category.name:<15} "
            f"${transaction.amount:>9.2f} "
            f"{transaction.detail:<25} "
            f"{balance.summary()}"
        )


@dataclass(frozen=True)
class LowBalanceAlert:
    """Records the balance and transaction that triggered a low balance."""

    balance: Balance
    transaction: Transaction


class LowBalanceAlertObserver(BalanceObserver):
    """Raises an alert while the balance is below a threshold.

    The alert is raised only when the balance is strictly below the
    threshold, so a balance exactly equal to it does not trigger an alert.

    Args:
        threshold: The balance below which an alert is raised.
        on_alert: Optional callback called with the LowBalanceAlert at the
            moment the balance drops below the threshold.
        on_recover: Optional callback called with the Balance at the moment
            it returns to the threshold or above.
    """

    def __init__(
        self,
        threshold,
        on_alert: Callable[[LowBalanceAlert], None] | None = None,
        on_recover: Callable[[Balance], None] | None = None,
    ):
        self.threshold = threshold
        self.on_alert = on_alert
        self.on_recover = on_recover
        self.low_balance_alert = None

    def update(
        self,
        balance: Balance,
        transaction: Transaction,
        reversal: bool = False,
    ):
        was_low = self.alert_triggered()
        if balance.get_balance() < self.threshold:
            self.low_balance_alert = LowBalanceAlert(balance, transaction)
            if not was_low and self.on_alert is not None:
                self.on_alert(self.low_balance_alert)
        else:
            self.low_balance_alert = None
            if was_low and self.on_recover is not None:
                self.on_recover(balance)

    def alert_triggered(self) -> bool:
        """Return True if the balance is currently below the threshold."""
        return self.low_balance_alert is not None
