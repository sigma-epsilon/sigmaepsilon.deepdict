# -*- coding: utf-8 -*-
import unittest

from linkeddeepdict import LinkedDeepDict


class TestDeepDict(unittest.TestCase):

    def test_deepdict(self):
        """
        Qualitative test on basic usage of a LinkedDeepDict.
        """
        data = LinkedDeepDict()
        data['a', 'b', 'c'] = 1
        f = data.containers
        assert [c.key for c in f(inclusive=True, deep=True)] == [
            None, 'a', 'b']
        assert [c.key for c in f(inclusive=True, deep=False)] == [None, 'a']
        assert [c.key for c in f(inclusive=False, deep=True)] == ['a', 'b']
        assert [c.key for c in f(inclusive=False, deep=False)] == ['a']
        assert data['a', 'b'].depth == 2
        assert data['a', 'b'].key == 'b'
        assert data.is_root() is True
        assert data['a', 'b'].is_root() is False
        assert data['a', 'b'].parent == data['a']
        assert data['a', 'b'].root() == data

        # lock test
        has_error = False
        data.lock()
        assert data.locked
        try:
            data['a', 'b', 'd'] = 2
        except:
            has_error = True
        finally:
            assert has_error
        data.unlock()
        assert not data.locked
        has_error = False
        try:
            data['a', 'b', 'd'] = 2
        except:
            has_error = True
        finally:
            assert not has_error

        # try indexing
        data['a']['b']['e'] = 3
        assert data['a', 'b', 'e'] == 3
        
        # other stuff
        data['a', 'b'].root()
        data.__repr__()
        
    def test_contains(self):
        data = LinkedDeepDict()
        data['a', 'b', 'c'] = 1
        self.assertTrue(["a", "b", "c"] in data)
        self.assertTrue("a" in data)

    def test_lib_compliance(self):
        """
        Tests to assure that a `LinkedDeepDict` works the same way as a `dict`.
        """
        data1 = LinkedDeepDict(a=1, b=dict(c=2, d=3))
        data2 = dict(a=1, b=dict(c=2, d=3))
        assert data1 == data2
        assert list(data1.keys()) == list(data1.keys())
        assert list(data1.values()) == list(data1.values())
        
        
if __name__ == "__main__":
    unittest.main()
