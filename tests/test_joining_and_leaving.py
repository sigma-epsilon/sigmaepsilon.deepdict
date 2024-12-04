# -*- coding: utf-8 -*-
import unittest
import pytest

from sigmaepsilon.deepdict import DeepDict


class TestJoiningAndLeaving(unittest.TestCase):
    def test_join_parent_deprecation_warning(self):
        dd = DeepDict()
        with pytest.warns(
            DeprecationWarning, match="The __join_parent__ method is deprecated."
        ):
            dd.__join_parent__(None, None)

    def test_leave_parent_deprecation_warning(self):
        dd = DeepDict()
        with pytest.warns(
            DeprecationWarning, match="The __leave_parent__ method is deprecated."
        ):
            dd.__leave_parent__()

    def test_before_join_parent(self):

        counter = 0

        class MyDeepDict(DeepDict):
            def __before_join_parent__(self, *args) -> None:
                nonlocal counter
                counter += 1
                return super().__before_join_parent__(*args)

        parent = MyDeepDict()
        child = MyDeepDict()
        parent["A"] = child
        self.assertEqual(counter, 1)
        self.assertIs(parent, child.parent)
        self.assertEqual("A", child.key)

    def test_after_join_parent(self):

        counter = 0

        class MyDeepDict(DeepDict):
            def __after_join_parent__(self, *args) -> None:
                nonlocal counter
                counter += 1
                return super().__after_join_parent__(*args)

        parent = MyDeepDict()
        child = MyDeepDict()
        parent["A"] = child
        self.assertEqual(counter, 1)
        self.assertIs(parent, child.parent)
        self.assertEqual("A", child.key)

    def test_before_leave_parent(self):

        counter = 0

        class MyDeepDict(DeepDict):
            def __before_leave_parent__(self) -> None:
                nonlocal counter
                counter += 1
                return super().__before_leave_parent__()

        parent = MyDeepDict()
        child = MyDeepDict()
        parent["A"] = child
        del parent["A"]
        self.assertEqual(counter, 1)
        self.assertIsNone(child.parent)
        self.assertIsNone(child.key)
        self.assertTrue(child.is_root())

    def test_after_leave_parent(self):

        counter = 0

        class MyDeepDict(DeepDict):
            def __after_leave_parent__(self) -> None:
                nonlocal counter
                counter += 1
                return super().__after_leave_parent__()

        parent = MyDeepDict()
        child = MyDeepDict()
        parent["A"] = child
        del parent["A"]
        self.assertEqual(counter, 1)
        self.assertIsNone(child.parent)
        self.assertIsNone(child.key)
        self.assertTrue(child.is_root())


if __name__ == "__main__":
    unittest.main()
