# -*- coding: utf-8 -*-
import unittest
import unittest.mock

from sigmaepsilon.deepdict import DeepDict, Key


class TestDelitem(unittest.TestCase):
    def test_delitem_1(self):
        dd = DeepDict()
        dd["A", "B"] = DeepDict()
        del dd["A", "B"]
        keys = list(dd.keys())
        self.assertTrue(len(keys) == 1)
        self.assertEqual(keys[0], "A")

    def test_delitem_2(self):
        from sigmaepsilon.deepdict import DeepDict

        dd = DeepDict()
        dd["A", "B"] = DeepDict()
        del dd["A"]
        keys = list(dd.keys())
        self.assertTrue(len(keys) == 0)
        
    def test_delitem_3(self):
        
        counter = 0
        
        class MyDeepDict(DeepDict):
            def __leave_parent__(self) -> None:
                nonlocal counter
                counter += 1
                return super().__leave_parent__()
        
        dd = MyDeepDict()
        dd["A"] = MyDeepDict()
        del dd["A"]
        self.assertEqual(counter, 1)
        
    def test_delitem_4(self):
        
        counter = 0
        
        class MyDeepDict(DeepDict):
            def __leave_parent__(self) -> None:
                nonlocal counter
                counter += 1
                return super().__leave_parent__()
        
        dd = MyDeepDict()
        dd["A", "B"] = MyDeepDict()
        counter = 0
        del dd["A", "B"]
        self.assertEqual(counter, 1)
        
    def test_delitem_5(self):
        
        counter = 0
        
        class MyDeepDict(DeepDict):
            def __leave_parent__(self) -> None:
                nonlocal counter
                counter += 1
                return super().__leave_parent__()
        
        dd = MyDeepDict()
        dd[Key((1, 2))] = MyDeepDict()
        counter = 0
        del dd[Key((1, 2))]
        self.assertEqual(counter, 1)
        


if __name__ == "__main__":
    unittest.main()
