# -*- coding: utf-8 -*-
from typing import Iterable, Tuple, Any, List, Hashable, Optional, Union, TypeVar, Callable
from copy import copy

try:
    import asciitree
except ImportError:
    asciitree = None

__all__ = ["dictparser", "parseaddress", "parseitems", "parsedicts", "parsedicts_addr"]


DictLike = TypeVar("DictLike")


def dictparser(d: dict, *, dtype=dict, **_kw) -> Iterable[Tuple[List[Hashable], Any]]:
    """
    Iterates through all the values of a nested dictionary.

    Notes
    -----
    Returns all kinds of items, even nested discionaries themselves,
    along with their content.

    Example
    -------
    >>> from sigmaepsilon.deepdict import dictparser
    >>> d = {
    ...     "a" : {"aa" : 1},
    ...     "b" : 2,
    ...     "c" : {"cc" : {"ccc" : 3}},
    ... }
    >>> for address, value in dictparser(d):
    ...     print(f"Address: {address}, Value: {value}")
    Address: ['a', 'aa'], Value: 1
    Address: ['b'], Value: 2
    Address: ['c', 'cc', 'ccc'], Value: 3
    """
    address = _kw.get("_addr", [])
    for key, value in d.items():
        subaddress = copy(address)
        subaddress.append(key)
        if isinstance(value, dtype):
            for data in dictparser(value, dtype=dtype, _addr=subaddress):
                yield data
        else:
            yield subaddress, value


def parseaddress(d: dict, address: List[Hashable]) -> Any:
    """
    Returns a value specified with an address.

    Example
    -------
    >>> from sigmaepsilon.deepdict import parseaddress
    >>> d = {
    ...     "a" : {"aa" : 1},
    ...     "b" : 2,
    ...     "c" : {"cc" : {"ccc" : 3}},
    ... }
    >>> parseaddress(d, ['c', 'cc', 'ccc'])
    3
    """
    if not isinstance(d, dict):
        raise ValueError

    if not address[0] in d:
        raise KeyError(address[0])

    if len(address) > 1:
        return parseaddress(d[address[0]], address[1:])
    else:
        return d[address[0]]


def parseitems(d: dict, *, dtype: Any = dict) -> Iterable[Tuple[Hashable, Any]]:
    """
    A generator function that yields all the items of a nested dictionary as
    (key, value) pairs.

    Notes
    -----
    Does not return nested dictionaries themselves, only their content.

    Example
    -------
    >>> from sigmaepsilon.deepdict import parseitems
    >>> d = {
    ...     "a" : {"aa" : 1},
    ...     "b" : 2,
    ...     "c" : {"cc" : {"ccc" : 3}},
    ... }
    >>> for key, value in parseitems(d):
    ...     print(f"Key: {key}, Value: {value}")
    Key: aa, Value: 1
    Key: b, Value: 2
    Key: ccc, Value: 3
    """
    for key, value in d.items():
        if isinstance(value, dtype):
            for data in parseitems(value, dtype=dtype):
                yield data
        else:
            yield key, value


def parsedicts(
    d: dict, *, inclusive: bool = True, dtype: Any = dict, deep: bool = True
) -> Iterable[dict]:
    """
    Returns all subdirectories of a dictionary.

    Example
    -------
    >>> from sigmaepsilon.deepdict import parsedicts
    >>> d = {
    ...     "a" : {"aa" : 1},
    ...     "b" : 2,
    ...     "c" : {"cc" : {"ccc" : 3}},
    ... }

    >>> for subd in parsedicts(d):
    ...     print(subd)
    {'a': {'aa': 1}, 'b': 2, 'c': {'cc': {'ccc': 3}}}
    {'aa': 1}
    {'cc': {'ccc': 3}}
    {'ccc': 3}

    >>> for subd in parsedicts(d, inclusive=False):
    ...     print(subd)
    {'aa': 1}
    {'cc': {'ccc': 3}}
    {'ccc': 3}
    """
    if inclusive:
        if isinstance(d, dtype):
            yield d

    for value in d.values():
        if isinstance(value, dtype):
            yield value
            if deep:
                for subvalue in parsedicts(value, inclusive=False, dtype=dtype):
                    yield subvalue


def parsedicts_addr(
    d: dict, *, inclusive: bool = True, dtype: Any = dict, deep: bool = True, **_kw
) -> Tuple[List[Hashable], Iterable[dict]]:
    """
    Returns all subdirectories of a dictionary and their addresses.

    Example
    -------
    >>> from sigmaepsilon.deepdict import parsedicts_addr
    >>> d = {
    ...     "a" : {"aa" : 1},
    ...     "b" : 2,
    ...     "c" : {"cc" : {"ccc" : 3}},
    ... }

    >>> for addr, subd in parsedicts_addr(d):
    ...     print(f"{subd} @ {addr}")
    {'a': {'aa': 1}, 'b': 2, 'c': {'cc': {'ccc': 3}}} @ []
    {'aa': 1} @ ['a']
    {'cc': {'ccc': 3}} @ ['c']
    {'ccc': 3} @ ['c', 'cc']

    >>> for addr, subd in parsedicts_addr(d, inclusive=False):
    ...     print(f"{subd} @ {addr}")
    {'aa': 1} @ ['a']
    {'cc': {'ccc': 3}} @ ['c']
    {'ccc': 3} @ ['c', 'cc']
    """
    address = _kw.get("_addr", [])

    if inclusive:
        if isinstance(d, dtype):
            yield address, d

    for key, value in d.items():
        if isinstance(value, dtype):
            addr = copy(address)
            addr.append(key)
            yield addr, value
            if deep:
                for subaddr, subval in parsedicts_addr(
                    value, inclusive=False, dtype=dtype, _addr=addr
                ):
                    yield subaddr, subval


def _asciitree(data: dict, dtype: type = dict, **_kw) -> dict:
    tree = _kw.get("_tree", {})
    name = getattr(data, "name", data.__class__.__name__)
    name = data.__class__.__name__ if name is None else name
    tree[name] = {}
    for value in data.values():
        if isinstance(value, dtype):
            _asciitree(value, dtype=dtype, _tree=tree[name])
    return tree


def _wrap(data: dict, wrapper: DictLike, tr:Optional[Union[Callable, None]]=None, **_kw) -> DictLike:
    result = _kw.get("_result", None)
    if result is None:
        result = wrapper()
        
    if tr is None:
        tr = lambda x: x
        
    for key, value in data.items():
        if isinstance(value, dict):
            result[key] = wrapper()
            _wrap(value, wrapper, tr=tr, _result=result[key])
        else:
            result[key] = tr(value)
            
    return result


if asciitree is None:  # pragma: no cover

    def asciiprint(*_, **__) -> str:
        raise ImportError("This requires the 'asciitree' package.")


else:

    def asciiprint(
        data: dict,
        *,
        dtype: Optional[Union[type, None]] = None,
        tr: Optional[Union[asciitree.KeyArgsConstructor, None]] = None,
    ) -> None:
        """
        Prints a dictionary as a tree using the ASCII character set.

        Parameters
        ----------
        data: dict, Optional
            A dictionary.
        dtype: type, Optional
            If a valid type is provided (a subclass of `dict`), then the tree
            will only include containers of that class. Default is None, in which case
            only containers with the same type as 'data' are included in the output.
        tr: asciitree.KeyArgsConstructor, Optional
            A formatter to use. Default is None, in which case a `asciitree.LeftAligned`
            instance is created at runtime.

        Notes
        -----
        This requires the `asciitree` package to be installed.

        Example
        -------
        >>> from sigmaepsilon.deepdict import DeepDict, asciiprint
        >>> d = {
        ...     "a" : {"aa" : 1},
        ...     "b" : 2,
        ...     "c" : {"cc" : {"ccc" : 3}},
        ... }
        >>> data = DeepDict.wrap(d)
        >>> asciiprint(data)
        DeepDict
         +-- a
         +-- c
             +-- cc
        """
        dtype = data.__class__ if dtype is None else dtype
        
        if not isinstance(data, dict):
            raise TypeError("Type of 'data' must be a subclass of 'dict'")
        
        if not issubclass(dtype, dict):
            raise TypeError("'dtype' must be a subclass of 'dict'")

        tr = asciitree.LeftAligned() if tr is None else tr

        print(tr(_asciitree(data)))
