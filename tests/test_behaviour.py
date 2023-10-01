# -*- coding: utf-8 -*-
import unittest

from sigmaepsilon.core.testing import SigmaEpsilonTestCase
from sigmaepsilon.deepdict import DeepDict, Key, Value


class TestBehaviour(SigmaEpsilonTestCase):
    def test_behaviour_1(self):
        d = DeepDict()
        d[Key((1, 2))] = "A"
        self.assertEqual(d[Key((1, 2))], "A")
        self.assertFalse((1, 2) in d)
        self.assertTrue(Key((1, 2)) in d)
        del d[Key((1, 2))]
        self.assertFalse(Key((1, 2)) in d)
        d[Key((1, 2))] = "A"
        d[Key((1, 2))] = None

    def test_behaviour_2(self):
        d = DeepDict()
        d[1, 2] = "A"
        self.assertTrue((1, 2) in d)

    def test_behaviour_3(self):
        data = DeepDict()
        data["a", "b", "c", "e"] = 1
        self.assertEqual(data["a", "b", "c"].parent.key, "b")
        self.assertFalse(data["a", "b", "c"].is_root())
        self.assertTrue(data["a", "b", "c"].is_leaf())

    def test_behaviour_4(self):
        data = DeepDict()
        data["a", "b", "c", "e"] = 1
        data.lock()
        self.assertTrue(data.locked)

        def foo():
            data["b"] = 1

        self.assertFailsProperly(KeyError, foo)

    def test_behaviour_5(self):
        d = {
            "a": {"aa": 1},
            "b": 2,
            "c": {"cc": {"ccc": 3}},
        }

        def foo():
            DeepDict(d)["c", "cc", "ccc"]

        self.assertFailsProperly(AttributeError, foo)

    def test_behaviour_6(self):
        data = DeepDict()
        data["a", "b", "c", "e"] = Value(1)
        self.assertEqual(data["a", "b", "c"].parent.key, "b")
        self.assertFalse(data["a", "b", "c"].is_root())
        self.assertTrue(data["a", "b", "c"].is_leaf())

    def test_behaviour_7(self):
        data = DeepDict(a=1, b=DeepDict(c=2))
        data["d"] = 2
        self.assertEqual(data["d"], 2)
        self.assertEqual(data["b", "c"], 2)
        self.assertEqual(data["b"].address[0], "b")
        self.assertEqual(len(data.address), 0)

    def test_behaviour_8(self):
        data = DeepDict(a=1)

        def foo():
            [] in data

        self.assertFailsProperly(ValueError, foo)

    def test_behaviour_9(self):
        data = DeepDict()
        data["a", "b", "c", "e"] = 1
        data["a"]["b"]["d"] = 2
        b = data["a", "b"]
        b["e"] = 3
        b["f"] = 1, 2, 3

        for _ in data.keys(deep=True, return_address=True):
            pass

        for _ in data.values(deep=True, return_address=True):
            pass

        for _ in data.items(deep=True, return_address=True):
            pass

        for _ in data.keys(deep=True, return_address=False):
            pass

        for _ in data.values(deep=True, return_address=False):
            pass

        for _ in data.items(deep=True, return_address=False):
            pass

    def test_behaviour_10(self):
        data = DeepDict()
        data["a", "b", "c"] = 1
        self.assertTrue(data.name is None)
        self.assertEqual(data["a"].name, "a")

        data.name = "data"
        self.assertEqual(data.name, "data")
        self.assertFailsProperly(TypeError, lambda v: setattr(data, "name", v), 10)


if __name__ == "__main__":
    unittest.main()
