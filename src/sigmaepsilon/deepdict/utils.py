# -*- coding: utf-8 -*-
from typing import Iterable, Tuple, Any, List, Hashable
from copy import copy


__all__ = ["dictparser", "parseaddress", "parseitems", "parsedicts", "parsedicts_addr"]


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
