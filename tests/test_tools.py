# -*- coding: utf-8 -*-
import unittest

from linkeddeepdict.tools.kwargtools import isinkwargs, allinkwargs, anyinkwargs, \
    getfromkwargs, popfromkwargs, getallfromkwargs, getasany, countkwargs


class TestTools(unittest.TestCase):

    def test_kwargtools(self):
        kwargs = dict(a = 1, c = 2)
        assert isinkwargs('a', **kwargs)
        assert all(isinkwargs(['a', 'c'], **kwargs))
        assert not isinkwargs('b', **kwargs)
        assert not any(isinkwargs(['b', 'd'], **kwargs))
        assert any(isinkwargs(['a', 'b'], **kwargs))
        assert any(isinkwargs(['c', 'd'], **kwargs))
        assert allinkwargs(['a', 'c'], **kwargs)
        assert allinkwargs('a', **kwargs)
        assert anyinkwargs(['d', 'c'], **kwargs)
        assert anyinkwargs('c', **kwargs)
        assert getfromkwargs(['a'], None, int, **kwargs) == [1]
        assert getfromkwargs(['b'], None, None, **kwargs) == [None]
        assert getallfromkwargs(['a', 'c'], None, **kwargs) == [1, 2]
        assert getasany(['a', 'b'], None, **kwargs) == 1
        
        d = {'E1': 1, 'E2': 2, 'G12': 12, 'NU23': 0}
        nE = countkwargs(lambda s: s[0] == 'E', **d)
        nG = countkwargs(lambda s: s[0] == 'G', **d)
        nNU = countkwargs(lambda s: s[0:2] == 'NU', **d)
        assert nE == 2
        assert nG == 1
        assert nNU == 1
        popfromkwargs(['E1'], d)
        assert isinstance(popfromkwargs(['E2'], d, astype=float)[0], float)
        assert 'E1' not in d
               
        
if __name__ == "__main__":
    unittest.main()
