# -*- coding: utf-8 -*-
import unittest

from sigmaepsilon.core.testing import SigmaEpsilonTestCase
from sigmaepsilon.deepdict import DeepDict


class TestWrap(SigmaEpsilonTestCase):
    def test_wrap(self):
        d = {
            "a": {"aa": 1},
            "b": 2,
            "c": {"cc": {"ccc": 3}},
        }
        self.assertEqual(DeepDict.wrap(d)["a", "aa"], 1)
        self.assertEqual(DeepDict.wrap(d)["b"], 2)
        self.assertEqual(DeepDict.wrap(d)["c", "cc", "ccc"], 3)
        
        DeepDict.wrap(d, copy=True)
        DeepDict.wrap(d, deepcopy=True)
        
        self.assertFailsProperly(ValueError, DeepDict.wrap, d, copy=True, deepcopy=True)


if __name__ == "__main__":
    unittest.main()
