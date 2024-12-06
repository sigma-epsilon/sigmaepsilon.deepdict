import pytest
from sigmaepsilon.deepdict import DeepDict
from sigmaepsilon.deepdict.exceptions import DeepDictLockedError


def test_locked_setitem():
    dd = DeepDict()
    dd.lock()
    assert dd.locked
    key = "A"
    with pytest.raises(
        DeepDictLockedError, match=f"Missing key '{key}' and the object is locked!"
    ):
        dd[key] = 1
    dd.unlock()
    dd[key] = 1
    assert key in dd


def test_locked_delitem():
    dd = DeepDict()
    key = "A"
    dd[key] = 1
    dd.lock()
    assert dd.locked
    with pytest.raises(DeepDictLockedError, match="The object is locked!"):
        del dd[key]
    dd.unlock()
    del dd[key]
    assert key not in dd
