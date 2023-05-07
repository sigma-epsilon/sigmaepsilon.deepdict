# http://stackoverflow.com/a/6190500/562769
from typing import Hashable, Union, Tuple, Any
try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable
import six

from .tools.dtk import dictparser, parseitems, parseaddress, parsedicts


__all__ = ['LinkedDeepDict']


NoneType = type(None)


def issequence(arg) -> bool:
    return (
        isinstance(arg, Iterable)
        and not isinstance(arg, six.string_types)
    )  


class LinkedDeepDict(dict):
    """
    An nested dictionary class with a self-replicating default factory. 
    It can be a drop-in replacement for the bulit-in dictionary type, 
    but it's more capable as it handles nested layouts.
    
    Examples
    --------
    Basic usage:
    
    >>> from ldd import LinkedDeepDict
    >>> d = {'a' : {'aa' : {'aaa' : 0}}, 'b' : 1, 'c' : {'cc' : 2}}
    >>> dd = LinkedDeepDict(d)
    >>> list(dd.values(deep=True))
    [0, 1, 2]
    
    See the docs for more use cases!
        
    """
    
    def __init__(self, *args, parent:'LinkedDeepDict'=None, 
                 root:'LinkedDeepDict'=None, locked:bool=None, 
                 **kwargs):
        """
        Returns a `LinkedDeepDict` instance.

        Parameters
        ----------
        *args : tuple, Optional
            Extra positional arguments are forwarded to the `dict` class.

        parent : `LinkedDeepDict`, Optional
            Parent `LinkedDeepDict` instance. Default is `None`.

        root : `LinkedDeepDict`, Optional
            The top-level object. It is automatically set when creating nested
            layouts, but may be explicitly provided. Default is `None`. 

        locked : bool or NoneType, Optional
            If the object is locked, it reacts to missing keys as a regular dictionary would.
            If it is not, a new level and a new child is created (see the examples in the docs).
            A `None` value means that in terms of locking, the state of the object 
            is inherited from its parent. Default is `None`.

        **kwargs : tuple, Optional
            Extra keyword arguments are forwarded to the `dict` class.

        """
        for k, v in kwargs.items():
            if isinstance(v, LinkedDeepDict):
                v.parent = self
                v._key = k
        super().__init__(*args, **kwargs)
        self.parent = parent
        self._root = root
        self._locked = locked
        self._key = None
        
    @property
    def key(self) -> Union[Hashable, NoneType]:
        """
        Returns the key of the dictionary in its parent, or `None` if the 
        object is the root.
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
            return self._locked if isinstance(self._locked, bool) else self.parent.locked

    @property
    def depth(self) -> int:
        """
        Retuns the depth of the actual instance in a layout, starting from 0..
        """
        if self.parent is None:
            return 0
        else:
            return self.parent.depth + 1
        
    @property
    def address(self) -> Tuple:
        """Returns the address of an item."""
        if self.is_root():
            return []
        else:
            r = self.parent.address
            r.append(self.key)
            return r

    def lock(self):
        """
        Locks the layout of the dictionary. If a `LinkedDeepDict` is locked,
        missing keys are handled the same way as they would've been handled
        if it was a ´dict´. Also, setting or deleting items in a locked
        dictionary and not possible and you will experience an error upon trying.
        
        """
        self._locked = True

    def unlock(self):
        """
        Releases the layout of the dictionary. If a `LinkedDeepDict` is not locked,
        a missing key creates a new level in the layout, also setting and deleting
        items becomes an option.
        
        """
        self._locked = False
        
    def root(self):
        """
        Returns the top-level object in a nested layout.
        """
        if self.parent is None:
            return self
        else:
            if self._root is not None:
                return self._root
            else:
                return self.parent.root()

    def is_root(self) -> bool:
        """
        Returns `True`, if the object is the root.
        """
        return self.parent is None

    def containers(self, *args, inclusive:bool=False, deep:bool=True, 
                   dtype:Any=None, **kwargs):
        """
        Returns all the containers in a nested layout. A dictionary in a nested layout
        is called a container, only if it contains other containers (it is a parent). 

        Parameters
        ----------
        inclusive : bool, Optional
            If `True`, the object the call is made upon also gets returned.
            This can be important if you make the call on the root object, which most
            of the time does not hold onto relevant data directly.
            Default is `False`.

        deep : bool, Optional
            If `True` the parser goes into nested dictionaries.
            Default is `True`

        dtype : Any, Optional
            Constrains the type of the returned objects.
            Default is `None`, which means no restriction.

        Returns
        -------
        generator
            Returns a generator object.

        Examples
        --------
        A simple example:

        >>> from ldd import LinkedDeepDict
        >>> data = LinkedDeepDict()
        >>> data['a', 'b', 'c'] = 1
        >>> [c.key for c in data.containers()]
        ['a', 'b']

        We can see, that dictionaries 'a' and 'b' are returned as containers, but 'c' 
        isn't,  because it is not a parent, there are no deeper levels. 

        >>> [c.key for c in data.containers(inclusive=True, deep=True)]
        [None, 'a', 'b']

        >>> [c.key for c in data.containers(inclusive=True, deep=False)]     
        [None, 'a']

        >>> [c.key for c in data.containers(inclusive=False, deep=True)]       
        ['a', 'b']

        >>> [c.key for c in data.containers(inclusive=False, deep=False)]      
        ['a']

        """
        dtype = self.__class__ if dtype is None else dtype
        return parsedicts(self, inclusive=inclusive, dtype=dtype, deep=deep)

    def __getitem__(self, key):
        try:
            if issequence(key):
                return parseaddress(self, key)
            else:
                return super().__getitem__(key)
        except ValueError:
            return self.__missing__(key)
        except KeyError:
            return self.__missing__(key)
        
    def __delitem__(self, key):
        if self.locked:
            raise RuntimeError("The object is locked!")
        super().__delitem__(key)

    def __setitem__(self, key, value):
        if self.locked:
            raise RuntimeError("The object is locked!")
        try:
            if issequence(key):
                if not key[0] in self:
                    d = self.__missing__(key[0])
                else:
                    d = self[key[0]]
                if len(key) > 1:
                    d.__setitem__(key[1:], value)
                else:
                    d = self[key[0]]
                    if isinstance(d, LinkedDeepDict):
                        d.__leave_parent__()
                    if value is None:
                        del self[key[0]]
                    else:
                        self[key[0]] = value
            else:
                if key in self:
                    d = self[key]
                    if isinstance(d, LinkedDeepDict):
                        d.__leave_parent__()
                if value is None:
                    if key in self:
                        del self[key]
                else:
                    if isinstance(value, LinkedDeepDict):
                        value.__join_parent__(self, key)
                    return super().__setitem__(key, value)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.locked:
            raise KeyError("Missing key : {}".format(key))
        if issequence(key):
            if key[0] not in self:
                self[key[0]] = value = self.__class__()
            else:
                value = self[key[0]]
            if len(key) > 1:
                return value.__missing__(key[1:])
            else:
                return value
        else:
            self[key] = value = self.__class__()
            return value
        
    def __contains__(self, item: Any):
        if not isinstance(item, Hashable) and issequence(item):
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
        
    def __reduce__(self):
        return self.__class__, tuple(), None, None, self.items()
    
    def __repr__(self):
        frmtstr = self.__class__.__name__ + '(%s)'
        return frmtstr % (dict.__repr__(self))
       
    def __leave_parent__(self):
        self.parent = None
        self._root = None
        self._key = None
            
    def __join_parent__(self, parent, key: Hashable = None):
        self.parent = parent
        self._root = parent.root()
        self._key = key

    def items(self, *args, deep:bool=False, return_address:bool=False, **kwargs):
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

    def values(self, *args, deep:bool=False, return_address:bool=False, **kwargs):
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

    def keys(self, *args, deep:bool=False, return_address:bool=False, **kwargs):
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
