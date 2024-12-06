from typing import Hashable, Any, TypeVar, Generic, Iterator
from copy import copy as shallow_copy, deepcopy as deep_copy
from types import NoneType
import warnings

from sigmaepsilon.core import Wrapper

from .utils import dictparser, parseitems, parsedicts, _wrap, _issequence
from .exceptions import DeepDictLockedError

__all__ = ["DeepDict", "Key", "Value"]


_DT = TypeVar("_DT", bound="DeepDict", covariant=True)
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")
_VT1 = TypeVar("_VT1")


class Key(Wrapper):
    """
    Helper class for keys.
    """

    def __init__(self, arg: Any):
        super().__init__(wrap=arg)


class Value(Wrapper):
    """
    Helper class for values.
    """

    def __init__(self, arg: Any):
        super().__init__(wrap=arg)


class DeepDict(dict, Generic[_KT, _VT]):
    """
    An nested dictionary class with a self-replicating default factory.

    It can serve as a direct replacement for the built-in dictionary type,
    but offers more functionality by supporting nested structures.

    The class is a generic type, which means that you can specify the types
    of the keys and values the same way you would do with a standard dictionary.

    Parameters
    ----------
    *args*: tuple, Optional
        Extra positional arguments are forwarded to the `dict` class.
    **kwargs**: dictionary, Optional
        Extra keyword arguments are forwarded to the `dict` class.

    Examples
    --------
    Basic usage:

    >>> from sigmaepsilon.deepdict import DeepDict
    >>> d = {'a' : {'aa' : {'aaa' : 0}}, 'b' : 1.0, 'c' : {'cc' : 2.0}}
    >>> dd = DeepDict.wrap(d)
    >>> list(dd.values(deep=True))
    [0, 1.0, 2.0]

    Getting values of a specific type:

    >>> list(dd.values(deep=True, vtype=int))
    [0]

    >>> list(dd.values(deep=True, vtype=float))
    [1.0, 2.0]

    Array-like access:

    >>> dd['a', 'aa', 'aaa']
    0

    Not that array-like access only works in this case because the original
    dictionary `d` was wrapped. If you create the instance like this,

    code-block:: python
        >>> dd = DeepDict(d)

    array-like access will not work and you will see a `KeyError`.

    """

    __slots__ = ["_parent", "_locked", "_key", "_name"]

    def __init__(self, *args, **kwargs):
        self._parent = None
        self._locked = None
        self._key = None
        self._name = None

        for k, v in kwargs.items():
            if isinstance(v, DeepDict):
                v._parent = self
                v._key = k

        deepdict_kwargs = {k: v for k, v in kwargs.items() if isinstance(v, DeepDict)}
        not_deepdict_kwargs = {
            k: v for k, v in kwargs.items() if not isinstance(v, DeepDict)
        }
        super().__init__(*args, **not_deepdict_kwargs)
        for k, v in deepdict_kwargs.items():
            self[k] = v

    @property
    def parent(self: _DT) -> _DT | NoneType:
        """
        Returns the parent of the instance, or None if it has no parent.
        """
        return self._parent

    @property
    def root(self: _DT) -> _DT:
        """
        Returns the top-level object in a nested layout.
        """
        if self.parent is None:
            return self
        else:
            return self.parent.root

    @property
    def name(self) -> str | NoneType:
        """
        The name of the dictionary. It is used for representation purposes.
        If a name is not specified, the `key` is returned here. Setting a name
        may be important for the top level entity, since it has no key.
        """
        if self._name is None:
            return self._key
        else:
            return self._name

    @name.setter
    def name(self, value: str) -> NoneType:
        if not isinstance(value, str):
            raise TypeError(f"Name must be a string, it is {type(value)}")
        self._name = value

    @property
    def key(self) -> _KT | NoneType:
        """
        Returns the key of the instance, or `None` if it has no parent.
        """
        return self._key

    @property
    def locked(self) -> bool:
        """
        Returns `True` if the object is locked. The property is equpped with a setter.
        """
        if self.parent is None:
            return self._locked if isinstance(self._locked, bool) else False
        else:
            return (
                self._locked if isinstance(self._locked, bool) else self.parent.locked
            )

    @property
    def depth(self) -> int:
        """
        Retuns the depth of the actual instance in a layout, starting from 0.
        """
        if self.parent is None:
            return 0
        else:
            return self.parent.depth + 1

    @property
    def address(self) -> tuple | NoneType:
        """Returns the address of an item or `None` it has no parent."""
        if self.is_root():
            return []
        else:
            r = self.parent.address
            r.append(self.key)
            return r

    @classmethod
    def wrap(cls, d: dict, copy: bool = False, deepcopy: bool = False) -> _DT:
        """
        Wraps a dictionary with all nested dictionaries and content.

        Parameters
        ----------
        d: dict
            The dictionary to wrap.
        copy: bool, Optional
            If `True`, shallow copies of the values are stored. Default is False.
        deepcopy: bool, Optional
            If `True`, deep copies of the values are stored. Default is False.

        Example
        -------
        >>> from sigmaepsilon.deepdict import DeepDict
        >>> d = {
        ...     "a" : {"aa" : 1},
        ...     "b" : 2,
        ...     "c" : {"cc" : {"ccc" : 3}},
        ... }
        >>> DeepDict.wrap(d)["c", "cc", "ccc"]
        3

        >>> list(DeepDict.wrap(d).items(deep=True))
        [('aa', 1), ('b', 2), ('ccc', 3)]

        """
        if copy and deepcopy:
            raise ValueError("Only one of 'copy' and 'deepcopy' can be True.")

        tr = None

        if copy:
            tr = shallow_copy

        if deepcopy:
            tr = deep_copy

        return _wrap(d, cls, tr=tr)

    def lock(self) -> NoneType:
        """
        Locks the layout of the dictionary. If a `DeepDict` is locked,
        missing keys are handled the same way as they would've been handled
        if it was a ´dict´. Also, setting or deleting items in a locked
        dictionary and not possible and you will experience an error upon trying.
        """
        self._locked = True

    def unlock(self) -> NoneType:
        """
        Releases the layout of the dictionary. If a `DeepDict` is not locked,
        a missing key creates a new level in the layout, also setting and deleting
        items becomes an option.
        """
        self._locked = False

    def is_root(self) -> bool:
        """
        Returns `True`, if the instance is the root.
        """
        return self.parent is None

    def is_leaf(self: _DT, dtype: Any = None) -> bool:
        """
        Returns `True`, if the instance has no children.

        Parameters
        ----------
        dtype: Any, Optional
            It can be a type that controls what is considered as a children.
            It is None by default, which means that only instances of the same
            class are considered children. In this case, a simple `dict` wouldn't
            make it.

        Example
        -------
        >>> from sigmaepsilon.deepdict import DeepDict
        >>> d = {
        ...     "a" : {"aa" : 1},
        ...     "b" : 2,
        ...     "c" : {"cc" : {"ccc" : 3}},
        ... }
        >>> dd = DeepDict.wrap(d)
        >>> dd.is_leaf(), dd["a"].is_leaf()
        (False, True)

        """
        dtype = self.__class__ if dtype is None else dtype
        return not any(list([isinstance(v, dtype) for v in self.values()]))

    def containers(
        self: _DT,
        *,
        inclusive: bool = False,
        deep: bool = True,
        dtype: Any = None,
    ) -> Iterator[_DT]:
        """
        Returns all the containers in a nested layout. A dictionary in a nested layout
        is called a container, only if it contains other containers (it is a parent).

        Parameters
        ----------
        inclusive: bool, Optional
            If `True`, the object the call is made upon also gets returned.
            This can be important if you make the call on the root object, which most
            of the time does not hold onto relevant data directly.
            Default is `False`.
        deep: bool, Optional
            If `True` the parser goes into nested dictionaries.
            Default is `True`
        dtype: Any, Optional
            Constrains the type of the returned objects.
            Default is `None`, which means no restriction.

        Returns
        -------
        generator
            Returns a generator object.

        Examples
        --------
        A simple example:

        >>> from sigmaepsilon.deepdict import DeepDict
        >>> data = DeepDict()
        >>> data['a', 'b', 'c'] = 1
        >>> [c.key for c in data.containers()]
        ['a', 'b']

        We can see, that dictionaries 'a' and 'b' are returned as containers, but 'c'
        isn't,  because it is not a parent, there are no deeper levels.

        With the `inclusive` parameter set to `True`, the object the call is made upon
        is also returned. Since the root of the layout has no parent, its key is `None`.

        >>> [c.key for c in data.containers(inclusive=True, deep=True)]
        [None, 'a', 'b']

        A few more examples:

        >>> [c.key for c in data.containers(inclusive=True, deep=False)]
        [None, 'a']

        >>> [c.key for c in data.containers(inclusive=False, deep=True)]
        ['a', 'b']

        >>> [c.key for c in data.containers(inclusive=False, deep=False)]
        ['a']

        """
        dtype = self.__class__ if dtype is None else dtype
        return parsedicts(self, inclusive=inclusive, dtype=dtype, deep=deep)

    def __getitem__(self: _DT, key: _KT, /) -> _VT:
        if isinstance(key, Key) or not _issequence(key):
            _key = key.wrapped if isinstance(key, Key) else key
            return dict.__getitem__(self, _key)
        else:
            item = self.__getitem__(key[0])
            if len(key) > 1:
                return item.__getitem__(key[1:])
            else:
                return item

    def __delitem__(self, key: _KT, /) -> NoneType:
        if isinstance(key, Key) or not _issequence(key):
            _key = key.wrapped if isinstance(key, Key) else key
            value = self[_key]
            value_is_DeepDict = isinstance(value, DeepDict)
            if value_is_DeepDict:
                value.__before_leave_parent__()
            if self.locked:
                raise DeepDictLockedError()
            dict.__delitem__(self, _key)
            if value_is_DeepDict:
                value.__after_leave_parent__()
        else:
            parent = self.__getitem__(key[:-1])
            parent.__delitem__(key[-1])

    def __setitem__(self, key: _KT, value: _VT, /) -> NoneType:
        if isinstance(key, Key) or not _issequence(key):
            _key = key.wrapped if isinstance(key, Key) else key
            if not isinstance(_key, Hashable):
                raise TypeError(f"Invalid key type: {type(_key)}")

            if key in self:
                self.__delitem__(key)
            elif self.locked:
                raise DeepDictLockedError(f"Missing key '{key}' and the object is locked!")

            value_is_DeepDict = isinstance(value, DeepDict)

            if value_is_DeepDict:
                value.__before_join_parent__(self, key)
            dict.__setitem__(self, _key, value)
            if value_is_DeepDict:
                value.__after_join_parent__(self, key)
        elif _issequence(key):
            if len(key) == 1:
                self.__setitem__(key[0], value)
            else:
                host = self.__missing__(key[0]) if key[0] not in self else self[key[0]]
                host.__setitem__(key[1:], value)
        else:  # pragma: no cover
            raise TypeError(f"Invalid key type: {type(key)}")

    def __missing__(self: _DT, key: _KT, /) -> _DT:
        """
        This is called when a value is about to be set and the key spans
        multiple levels. It creates the missing levels and returns the
        last level, so that the value can be set.
        """
        if self.locked:
            raise DeepDictLockedError(f"Missing key '{key}' and the object is locked!")

        if isinstance(key, Key) or not _issequence(key):
            value = self.__class__()
            _key = key.wrapped if isinstance(key, Key) else key
            self[_key] = value
            return value
        elif _issequence(key):
            if key[0] not in self:
                value = self.__class__()
                self[key[0]] = value
            else:
                value = self[key[0]]

            if len(key) > 1:
                if not isinstance(value, DeepDict):
                    raise TypeError(f"The value of key '{key[0]}' is not a DeepDict!")

                return value.__missing__(key[1:])
            else:
                return value

    def __contains__(self, item: Any, /) -> bool:
        if isinstance(item, Key):
            return super().__contains__(item.wrapped)
        elif isinstance(item, DeepDict):
            return (not item.is_root()) and (item.parent is self)
        elif _issequence(item):
            if len(item) == 0:
                raise ValueError(f"{item} has zero length")
            else:
                obj = self
                for subitem in item:
                    if not isinstance(subitem, Hashable):
                        raise TypeError(f"{subitem} is not hashable")
                    else:
                        if obj.__contains__(subitem):
                            obj = obj.__getitem__(subitem)
                        else:
                            return False
                return True
        elif isinstance(item, Hashable):
            return super().__contains__(item)
        else:
            raise TypeError(f"{item} is not hashable")

    def __reduce__(self) -> Any:
        return self.__class__, tuple(), None, None, self.items()

    def __repr__(self) -> str:
        frmtstr = self.__class__.__name__ + "(%s)"
        return frmtstr % (dict.__repr__(self))

    def _items(
        self: _DT, *, deep: bool = False, return_address: bool = False
    ) -> Iterator[tuple[_KT, _DT | _VT]]:
        if deep:
            if return_address:
                for addr, v in dictparser(self):
                    yield addr, v
            else:
                for k, v in parseitems(self):
                    yield k, v
        else:
            for k, v in super().items():
                yield k, v

    def items(
        self: _DT,
        *,
        deep: bool = False,
        return_address: bool = False,
        vtype: type = Any,
    ) -> Iterator[tuple[_KT, _DT | _VT]]:
        """
        Returns the items. When called without arguments, it works the same as for
        standard dictionaries.

        Parameters
        ----------
        deep: bool, Optional
            If `True` the parser goes into nested dictionaries.
            Default is `True`.
        return_address: bool, Optional
            If `True`, addresses are returned instead of keys. The difference is similar
            than that of absolute and repative paths. In this respect, keys are the relative
            paths (relative to the parent), and addresses are absolute paths (relative to the root).
            Default is False.
        vtype: type, Optional
            The type of the values to return. Default is `Any`.
        """
        if vtype is Any:
            for k, v in self._items(deep=deep, return_address=return_address):
                yield k, v
        else:
            for k, v in self._items(deep=deep, return_address=return_address):
                if isinstance(v, vtype):
                    yield k, v

    def _values(
        self: _DT, *, deep: bool = False, return_address: bool = False
    ) -> Iterator[_DT | _VT]:
        if deep:
            if return_address:
                for addr, v in dictparser(self):
                    yield addr, v
            else:
                for _, v in parseitems(self):
                    yield v
        else:
            for v in super().values():
                yield v

    def values(
        self: _DT,
        *,
        deep: bool = False,
        return_address: bool = False,
        vtype: _VT1 = Any,
    ) -> Iterator[_DT | _VT | _VT1]:
        """
        Returns the values. When called without arguments, it works the same as for
        standard dictionaries.

        Parameters
        ----------
        deep: bool, Optional
            If `True` the parser goes into nested dictionaries.
            Default is `True`.
        return_address: bool, Optional
            If `True`, addresses are returned as well.
            Default is False.
        vtype: type, Optional
            The type of the values to return. Default is `Any`.
        """
        if vtype is Any:
            for v in self._values(deep=deep, return_address=return_address):
                yield v
        else:
            for v in self._values(deep=deep, return_address=return_address):
                if isinstance(v, vtype):
                    yield v

    def keys(
        self: _DT,
        *,
        deep: bool = False,
        return_address: bool = False,
    ) -> Iterator[_KT]:
        """
        Returns the keys. When called without arguments, it works the same as for
        standard dictionaries.

        Parameters
        ----------
        deep: bool, Optional
            If `True` the parser goes into nested dictionaries.
            Default is `True`.
        return_address: bool, Optional
            If `True`, addresses are returned instead of keys. The difference is similar
            than that of absolute and repative paths. In this respect, keys are the relative
            paths (relative to the parent), and addresses are absolute paths (relative to the root).
            Default is False.
        """
        if deep:
            if return_address:
                for addr, _ in dictparser(self):
                    yield addr
            else:
                for k, _ in parseitems(self):
                    yield k
        else:
            for k in super().keys():
                yield k

    def __before_join_parent__(
        self: _DT, parent: _DT, key: _KT | NoneType = None
    ) -> NoneType:
        """Actions to be taken before joining a parent."""
        ...

    def __after_join_parent__(
        self: _DT, parent: _DT, key: _KT | NoneType = None
    ) -> NoneType:
        """
        Actions to be taken after joining a parent.

        .. note::
           If you implement this method, don't forget to call
           `super().__after_join_parent__()` as well.

        """
        self._parent = parent
        self._key = key

    def __before_leave_parent__(self) -> NoneType:
        """Actions to be taken before leaving a parent."""
        ...

    def __after_leave_parent__(self) -> NoneType:
        """
        Actions to be taken after leaving a parent.

        .. note::
           If you implement this method, don't forget to call
           `super().__after_leave_parent__()` as well.

        """
        self._parent = None
        self._key = None

    def __leave_parent__(self) -> NoneType:
        warnings.warn(
            "The __leave_parent__ method is deprecated. "
            "Please consult the documentation and use the "
            "__before_leave_parent__ and __after_leave_parent__ methods instead.",
            DeprecationWarning,
            stacklevel=2,
        )

    def __join_parent__(self: _DT, parent: _DT, key: _KT | NoneType = None) -> NoneType:
        warnings.warn(
            "The __join_parent__ method is deprecated. "
            "Please consult the documentation and use the "
            "__before_join_parent__ and __after_join_parent__ methods instead.",
            DeprecationWarning,
            stacklevel=2,
        )
