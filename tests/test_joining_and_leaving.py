# -*- coding: utf-8 -*-
import unittest
import pytest

from sigmaepsilon.deepdict import DeepDict, Key


class TestJoiningAndLeaving(unittest.TestCase):
    def test_join_parent_deprecation_warning(self):
        dd = DeepDict()
        with pytest.warns(DeprecationWarning, match="The __join_parent__ method is deprecated."):
            dd.__join_parent__(None, None)
            
    def test_leave_parent_deprecation_warning(self):
        dd = DeepDict()
        with pytest.warns(DeprecationWarning, match="The __leave_parent__ method is deprecated."):
            dd.__leave_parent__()


if __name__ == "__main__":
    unittest.main()
