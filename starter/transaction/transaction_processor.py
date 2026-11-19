"""Defines the TransactionProcessor, the invoker of the Command pattern."""

from command.command import Command


class TransactionProcessor:
    """Invoker: runs commands and remembers them so they can be undone."""

    def __init__(self):
        self._history: list[Command] = []

    @property
    def history(self) -> tuple[Command, ...]:
        """The commands executed so far, oldest first."""
        return tuple(self._history)

    def process(self, command: Command):
        """Execute a command and record it in the history."""
        command.execute()
        self._history.append(command)

    def process_all(self, commands):
        """Execute each command in order."""
        for command in commands:
            self.process(command)

    def undo_last(self) -> bool:
        """Undo the most recent command. Return False if there is none."""
        if not self._history:
            return False
        self._history.pop().undo()
        return True
