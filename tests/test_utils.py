# -*- coding: utf-8 -*-
import unittest

from sigmaepsilon.core.testing import SigmaEpsilonTestCase
from sigmaepsilon.core.decorate import suppress
from sigmaepsilon.deepdict import DeepDict, parseaddress, asciiprint


class TestPickle(SigmaEpsilonTestCase):
    def test_utils(self):
        data = DeepDict()
        self.assertFailsProperly(ValueError, parseaddress, [], "a")
        self.assertFailsProperly(KeyError, parseaddress, data, "a")

    def test_ascii(self):
        d = {
            "a": {"aa": 1},
            "b": 2,
            "c": {"cc": {"ccc": 3}},
        }
        data = DeepDict.wrap(d)
        suppress(asciiprint)(data)

        self.assertFailsProperly(TypeError, asciiprint, data, dtype=float)
        self.assertFailsProperly(TypeError, asciiprint, 10)


if __name__ == "__main__":
    unittest.main()
