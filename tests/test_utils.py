# -*- coding: utf-8 -*-
import unittest
import pickle

from sigmaepsilon.core.testing import SigmaEpsilonTestCase
from sigmaepsilon.deepdict import DeepDict, parseaddress


class TestPickle(SigmaEpsilonTestCase):
        
    def test_utils(self):
        data = DeepDict()        
        self.assertFailsProperly(ValueError, parseaddress, [], "a")
        self.assertFailsProperly(KeyError, parseaddress, data, "a")
                       
        
if __name__ == "__main__":
    unittest.main()