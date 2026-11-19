"""Defines the abstract Command used by the Command pattern."""

from abc import ABC, abstractmethod


class Command(ABC):
    """Encapsulates a request made against a receiver so it can be undone."""

    @abstractmethod
    def execute(self):
        """Carry out the command."""

    @abstractmethod
    def undo(self):
        """Reverse the effect of execute()."""
