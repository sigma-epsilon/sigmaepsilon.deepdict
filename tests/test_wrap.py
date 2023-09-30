# -*- coding: utf-8 -*-
import unittest

from sigmaepsilon.deepdict import DeepDict


class TestWrap(unittest.TestCase):
    def test_wrap(self):
        d = {
            "a": {"aa": 1},
            "b": 2,
            "c": {"cc": {"ccc": 3}},
        }
        self.assertEqual(DeepDict.wrap(d)["a", "aa"], 1)
        self.assertEqual(DeepDict.wrap(d)["b"], 2)
        self.assertEqual(DeepDict.wrap(d)["c", "cc", "ccc"], 3)


if __name__ == "__main__":
    unittest.main()
