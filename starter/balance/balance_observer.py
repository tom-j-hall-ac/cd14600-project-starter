"""Observers that react to changes in the Balance."""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from pattern.observer import Observer
from transaction.transaction import Transaction

if TYPE_CHECKING:
    from balance.balance import Balance


class BalanceObserver(Observer):
    """Interface for objects that want to be told about balance updates."""

    @abstractmethod
    def update(self, balance: Balance, transaction: Transaction):
        """Handle a balance update caused by a transaction."""


class PrintObserver(BalanceObserver):
    """Prints the balance summary after every transaction."""

    def update(self, balance: Balance, transaction: Transaction):
        print(balance.summary())


@dataclass(frozen=True)
class LowBalanceAlert:
    """Records the balance and transaction that triggered a low balance."""

    balance: Balance
    transaction: Transaction


class LowBalanceAlertObserver(BalanceObserver):
    """Raises an alert while the balance is below a threshold."""

    def __init__(self, threshold):
        self.threshold = threshold
        self.low_balance_alert = None

    def update(self, balance: Balance, transaction: Transaction):
        if balance.get_balance() < self.threshold:
            self.low_balance_alert = LowBalanceAlert(balance, transaction)
        else:
            self.low_balance_alert = None

    def alert_triggered(self) -> bool:
        """Return True if the balance is currently below the threshold."""
        return self.low_balance_alert is not None
