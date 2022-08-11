# -*- coding: utf-8 -*-
from copy import copy


def dictparser(d: dict = None, address=None, *args, dtype=dict, **kwargs):
    """
    Iterates through all the values of a nested dictionary.

    Notes
    -----
        Returns all kinds of items, even nested discionaries themselves,
        along with their content.
    """
    address = [] if address is None else address
    for key, value in d.items():
        subaddress = copy(address)
        subaddress.append(key)
        if isinstance(value, dtype):
            for data in dictparser(value, subaddress, dtype=dtype):
                yield data
        else:
            yield subaddress, value


def parseaddress(d: dict, a: list):
    """Returns a value specified with an address."""
    if not isinstance(d, dict):
        raise ValueError
    if not a[0] in d:
        raise KeyError(a[0])
    if len(a) > 1:
        return parseaddress(d[a[0]], a[1:])
    else:
        return d[a[0]]


def parseitems(d: dict = None, *args, dtype=dict, **kwargs):
    """
    A generator function that yields all the items of a nested dictionary as
    (key, value) pairs.

    Notes
    -----
        Does not return nested dictionaries themselves, only their content.
    """
    for key, value in d.items():
        if isinstance(value, dtype):
            for data in parseitems(value, dtype=dtype):
                yield data
        else:
            yield key, value


def parsedicts(d: dict = None, *args, inclusive=True, dtype=dict,
               deep=True, **kwargs):
    if inclusive:
        if isinstance(d, dtype):
            yield d
    for value in d.values():
        if isinstance(value, dtype):
            yield value
            if deep:
                for subvalue in \
                        parsedicts(value, inclusive=False, dtype=dtype):
                    yield subvalue
                    
                    
def parsedicts_addr(d: dict = None, address=[], *args, inclusive=True,
                    dtype=dict, deep=True, **kwargs):
    if inclusive:
        if isinstance(d, dtype):
            yield address, d
    for key, value in d.items():
        if isinstance(value, dtype):
            addr = copy(address)
            addr.append(key)
            yield addr, value
            if deep:
                for subaddr, subval in \
                    parsedicts_addr(value, addr,
                                    inclusive=False, dtype=dtype):
                    yield subaddr, subval
                    