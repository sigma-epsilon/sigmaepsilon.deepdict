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
        
    def test_behaviour_2(self):
        d = DeepDict()
        d[1, 2] = "A"
        self.assertTrue((1, 2) in d)
        
    def test_behaviour_3(self):
        data = DeepDict()
        data['a', 'b', 'c', 'e'] = 1
        self.assertEqual(data['a', 'b', 'c'].parent.key, "b")
        self.assertFalse(data['a', 'b', 'c'].is_root())
        self.assertTrue(data['a', 'b', 'c'].is_leaf())
        
    def test_behaviour_4(self):
        data = DeepDict()
        data['a', 'b', 'c', 'e'] = 1
        data.lock()
        self.assertTrue(data.locked)
        def foo(): data["b"] = 1
        self.assertFailsProperly(KeyError, foo)
        
    def test_behaviour_5(self):
        d = {
            "a" : {"aa" : 1},
            "b" : 2,
            "c" : {"cc" : {"ccc" : 3}}, 
        }
        def foo(): DeepDict(d)["c", "cc", "ccc"]
        self.assertFailsProperly(AttributeError, foo)
    
    def test_behaviour_6(self):
        data = DeepDict()
        data['a', 'b', 'c', 'e'] = Value(1)
        self.assertEqual(data['a', 'b', 'c'].parent.key, "b")
        self.assertFalse(data['a', 'b', 'c'].is_root())
        self.assertTrue(data['a', 'b', 'c'].is_leaf())
                       
        
if __name__ == "__main__":
    unittest.main()