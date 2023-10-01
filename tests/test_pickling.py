# -*- coding: utf-8 -*-
import unittest
import pickle

from sigmaepsilon.core.testing import SigmaEpsilonTestCase
from sigmaepsilon.deepdict import DeepDict


class TestPickle(SigmaEpsilonTestCase):
    def test_pickle(self):
        data = DeepDict()
        data["a", "b", "c", "e"] = 1
        data["a"]["b"]["d"] = 2
        b = data["a", "b"]
        b["e"] = 3
        b["f"] = 1, 2, 3

        serialized_obj = pickle.dumps(data)
        recreated_obj = pickle.loads(serialized_obj)

        self.assertIsInstance(recreated_obj, DeepDict)
        self.assertEqual(recreated_obj["a", "b", "d"], 2)


if __name__ == "__main__":
    unittest.main()
