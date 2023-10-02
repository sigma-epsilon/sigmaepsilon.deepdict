=================================================
Welcome to SigmaEpsilon.DeepDict's documentation!
=================================================

**Version**: |version|
  
**Useful links**:
:doc:`user_guide` |
:ref:`API Reference` |
`Source Repository <https://github.com/sigma-epsilon/sigmaepsilon.deepdict>`_

This is a lightweight Python library to manage nested dictionaries with 
parent-child relationships. The self replicating default factory makes the 
creation of complex nested layouts effortless using the :ref:`DeepDict` class. 
The library also provides a collection of useful algoritms for parsing of nested dictionaries. 
This architecture of data is utilized in many ``SigmaEpsilon`` projects.

Below you can find a small set of examples to get your attention. If you are interested,
take a look at the :doc:`user_guide` and the :ref:`API Reference`.

Installation
============

You can install the project from PyPI with `pip`:

.. code-block:: shell

   $ pip install sigmaepsilon.deepdict


Motivating examples
===================

Let say you have the following dictionary:

.. code-block:: python

   >>> d = {
   ...   "a" : {"aa" : 1},
   ...   "b" : 2,
   ...   "c" : {"cc" : {"ccc" : 3}}, 
   ... }

This is what happens when you iterate through the values of it:

.. code-block:: python

   >>> list(d.values())
   [{'aa': 1}, 2, {'cc': {'ccc': 3}}]

Everything goes as expected, the values of the dictionary are put into a list. 
See what happens if you use a :ref:`DeepDict` instead:

.. code-block:: python

   >>> from sigmaepsilon.deepdict import DeepDict
   >>> dd = DeepDict.wrap(d)
   >>> list(dd.values(deep=True))
   [1, 2, 3]

You see that by using the argument `deep=True`, the :ref:`DeepDict` instance goes into nested 
dictionaries and returns all the leafs. This way, the output `[1, 2, 3]` becomes independet
from the layout of your dictionary. It could have as many nested levels as you want
and still, it would always return only the leafs.

Another example for a possible use case is when you have to create a dictionary from dynamic
content, possibly only being realized at runtime. Let say we have a function that accepts two
arguments. The set of arguments for which the function have to be executed, is only known at
runtime. Take this case for example:

.. code-block:: python

   >>> categories = ["A", "B", "C"]
   >>> subcategories = ["1", "2", "3"]
   ...
   >>> def foo(cat, subcat):
   ...     # this is where you do your business
   ...     return "-".join([cat, subcat])

If you wanted to store the results using standard dictionaries, this is what you would do
(or something close to it):

.. code-block:: python

   >>> data = dict()
   >>> for cat in category:
   ...     if cat not in data:
   ...         data[cat] = dict()
   ...     for subcat in subcategory:
   ...         if subcat not in data[cat]:
   ...             data[cat][subcat] = dict()
   ...         data[cat, subcat] = foo(cat, subcat)
   >>> data["A"]["1"]
   "A-1"

In contrast, if you use a :ref:`DeepDict`, you can utilize the adopted indexing mechanism,
which makes using them feel like if they were arrays. Also, you don't have to worry about
KeyErrors here. De default factory handles everything for you.

.. code-block:: python

   >>> data = DeepDict()
   >>> for cat in category:
   ...     for subcat in subcategory:
   ...         data[cat, subcat] = foo(cat, subcat)  # data[cat][subcat] would also work
   >>> data["A", "1"]  # data["A"]["1"] would also work
   "A-1"

In fact, you can assign values as deep as you want:

.. code-block:: python

   >>> data = DeepDict()
   >>> data["a", 0, "b", 1, (5, 6)] = 10

Projects using :ref:`DeepDict`
==============================
The following projects all build on the :ref:`DeepDict` class:

- `SigmaEpsilon.Mesh <https://github.com/sigma-epsilon/sigmaepsilon.mesh>`__
   The `PolyData` class and other mesh data container classes are subclasses of :ref:`DeepDict`.

.. note::
   If you are using this library and you want your stuff to be listed here, get in contact
   with one of the maintainers of the project.

Contents
========

.. toctree::
   :maxdepth: 1

   user_guide
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
