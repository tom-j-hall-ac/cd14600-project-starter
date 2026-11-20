"""Defines the Observer pattern building blocks."""

from abc import ABC, abstractmethod


class Observer(ABC):
    """Interface for objects that want to be notified by a subject."""

    @abstractmethod
    def update(self, *args, **kwargs):
        """Standard update interface expected by the subject."""


class ObserverSubject:
    """Keeps a list of observers and notifies them when something changes."""

    def __init__(self):
        self._observers = []

    def register_observer(self, observer: Observer):
        """Subscribe an observer to future notifications."""
        self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        """Unsubscribe an observer."""
        self._observers.remove(observer)

    def clear_observers(self):
        """Unsubscribe every observer."""
        self._observers.clear()

    def notify(self, *args, **kwargs):
        """Pass the given arguments to every observer's update()."""
        for observer in self._observers:
            observer.update(*args, **kwargs)
