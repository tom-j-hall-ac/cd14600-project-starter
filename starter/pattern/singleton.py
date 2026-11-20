"""Defines a reusable Singleton base class enforced by a metaclass."""

import threading


class SingletonMeta(type):
    """Metaclass that creates at most one instance of each class.

    Because the check lives in the metaclass, calling the class directly,
    e.g. ``Balance()``, returns the same shared object as ``get_instance()``.
    ``__init__`` only runs for the first construction, so later calls never
    reset state. Arguments given to later calls are ignored.
    """

    _instances: dict = {}
    _lock = threading.RLock()

    def __call__(cls, *args, **kwargs):
        with SingletonMeta._lock:
            if cls not in SingletonMeta._instances:
                SingletonMeta._instances[cls] = super().__call__(
                    *args, **kwargs
                )
            return SingletonMeta._instances[cls]


class Singleton(metaclass=SingletonMeta):
    """Base class giving a class a single shared instance."""

    @classmethod
    def get_instance(cls):
        """Return the shared instance, creating it on first use."""
        return cls()
