"""Defines a reusable Singleton mixin."""


class Singleton:
    """Mixin giving a class a single shared instance via get_instance()."""

    _instance = None

    @classmethod
    def get_instance(cls):
        """Return the shared instance, creating it on first use."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
