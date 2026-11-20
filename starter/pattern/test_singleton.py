import unittest

from pattern.singleton import Singleton


class Counter(Singleton):
    """Singleton that counts how many times it is initialised."""

    initialisations = 0

    def __init__(self):
        Counter.initialisations += 1
        self.value = 0


class OtherSingleton(Singleton):
    pass


class TestSingleton(unittest.TestCase):

    def test_direct_construction_and_accessor_return_same_object(self):
        self.assertIs(Counter(), Counter.get_instance())

    def test_initialiser_runs_only_once(self):
        Counter()
        Counter.get_instance()
        Counter()
        self.assertEqual(Counter.initialisations, 1)

    def test_state_survives_repeated_construction(self):
        Counter.get_instance().value = 7
        self.assertEqual(Counter().value, 7)

    def test_each_subclass_has_its_own_instance(self):
        self.assertIsNot(Counter(), OtherSingleton())
        self.assertIsInstance(OtherSingleton(), OtherSingleton)


if __name__ == "__main__":
    unittest.main()
