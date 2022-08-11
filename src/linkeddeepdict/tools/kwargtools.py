# -*- coding: utf-8 -*-
try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable
from typing import Callable


def isinkwargs(keys, **kwargs):
    if isinstance(keys, Iterable) and not isinstance(keys, str):
        return [key in kwargs for key in keys]
    else:
        return keys in kwargs


def allinkwargs(keys, **kwargs):
    if isinstance(keys, Iterable) and not isinstance(keys, str):
        return all([key in kwargs for key in keys])
    else:
        return keys in kwargs


def anyinkwargs(keys, **kwargs):
    if isinstance(keys, Iterable) and not isinstance(keys, str):
        return any([key in kwargs for key in keys])
    else:
        return keys in kwargs


def getfromkwargs(keys, default=None, astype=None, **kwargs):
    res = [kwargs.get(k, default) for k in keys]
    if astype is None:
        return res
    else:
        return [astype(p) for p in res]


def popfromkwargs(keys, d: dict = None, *args, default=None, astype=None,
                **kwargs):
    res = [d.pop(k, default) for k in keys]
    if astype is None:
        return res
    else:
        return [astype(p) for p in res]


def getallfromkwargs(keys, default=None, **kwargs):
    params = getfromkwargs(keys, default=default, **kwargs)
    if None not in params:
        return params
    else:
        missing = list(filter(lambda p: p == default, params))
        if len(missing) == 1:
            key = keys[missing[0]]
            raise RuntimeError("Parameter {} is missing from the definition!"
                               .format(key))
        else:
            missing_keys = [keys[i] for i in missing]
            raise RuntimeError("Parameters {} is missing from the definition!"
                               .format(missing_keys))


def getasany(keys, default=None, **kwargs):
    try:
        condition = [key in kwargs for key in keys]
        if not any(condition) == True:
            return default
        return kwargs[keys[condition.index(True)]]
    except Exception:
        return None
    

def countkwargs(fnc: Callable, **kwargs):
    assert callable(fnc)
    return sum(list(map(fnc, kwargs.keys())))

