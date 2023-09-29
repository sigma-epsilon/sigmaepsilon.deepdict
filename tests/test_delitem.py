# -*- coding: utf-8 -*-
import unittest

from sigmaepsilon.deepdict import DeepDict


class TestDelitem(unittest.TestCase):

    def test_delitem_1(self):
        dd = DeepDict()
        dd['A', 'B'] = DeepDict()
        del dd['A', 'B']
        keys = list(dd.keys())
        self.assertTrue(len(keys) == 1)
        self.assertEqual(keys[0], "A")
        
    def test_delitem_2(self):
        from sigmaepsilon.deepdict import DeepDict
        dd = DeepDict()
        dd['A', 'B'] = DeepDict()
        del dd['A']
        keys = list(dd.keys())
        self.assertTrue(len(keys) == 0)
               
        
if __name__ == "__main__":
    unittest.main()