import pytest
from sigmaepsilon.deepdict import DeepDict, Key


def test_invalid_key_type():
    dd = DeepDict()
    with pytest.raises(TypeError, match=f"Invalid key type: {type([1,2])}"):
        dd[Key([1,2])] = 1
        
    with pytest.raises(TypeError, match=f"Invalid key type: {type({1:2})}"):
        dd[{1:2}] = 1
