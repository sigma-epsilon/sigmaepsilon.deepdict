import pytest
from sigmaepsilon.deepdict import DeepDict, Key
from sigmaepsilon.deepdict.exceptions import DeepDictLockedError


def test_missing_key_creates_new_deepdict():
    dd = DeepDict()
    missing_key = "new_key"
    result = dd.__missing__(missing_key)
    assert isinstance(result, DeepDict)
    assert missing_key in dd
    assert dd[missing_key] is result


def test_missing_key_creates_nested_deepdict():
    dd = DeepDict()
    missing_key = ("level1", "level2")
    result = dd.__missing__(missing_key)
    assert isinstance(result, DeepDict)
    assert "level1" in dd
    assert isinstance(dd["level1"], DeepDict)
    assert "level2" in dd["level1"]
    assert dd["level1"]["level2"] is result


def test_missing_key_with_key_wrapper():
    dd = DeepDict()
    missing_key = Key("wrapped_key")
    result = dd.__missing__(missing_key)
    assert isinstance(result, DeepDict)
    assert "wrapped_key" in dd
    assert dd["wrapped_key"] is result


def test_missing_key_when_locked_raises_DeepDictLockedError():
    dd = DeepDict()
    dd.lock()
    missing_key = "locked_key"
    with pytest.raises(
        DeepDictLockedError, match=f"Missing key '{missing_key}' and the object is locked!"
    ):
        dd.__missing__(missing_key)


def test_missing_key_with_sequence_when_locked_raises_DeepDictLockedError():
    dd = DeepDict()
    dd.lock()
    missing_key = "missing_key"
    with pytest.raises(
        DeepDictLockedError, match=f"Missing key '{missing_key}' and the object is locked!"
    ):
        dd.__missing__(missing_key)


def test_missing_key_with_first_key_not_missing():
    dd = DeepDict()
    dd["key1"] = DeepDict()
    missing_key = ("key1", "key2")
    result = dd.__missing__(missing_key)
    assert isinstance(result, DeepDict)
    assert "key1" in dd
    assert isinstance(dd["key1"], DeepDict)
    assert "key2" in dd["key1"]
    assert dd["key1"]["key2"] is result


def test_missing_not_able_to_create_second_level():
    dd = DeepDict()
    dd["key1"] = "value1"
    missing_key = ("key1", "key2")

    with pytest.raises(
        TypeError, match=f"The value of key '{missing_key[0]}' is not a DeepDict!"
    ):
        dd.__missing__(missing_key)
