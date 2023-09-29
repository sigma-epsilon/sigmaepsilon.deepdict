# **SigmaEpsilon.DeepDict**

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/sigma-epsilon/sigmaepsilon.deepdict/tree/main.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/sigma-epsilon/sigmaepsilon.deepdict/tree/main)
[![codecov](https://codecov.io/gh/sigma-epsilon/sigmaepsilon.deepdict/graph/badge.svg?token=7JKJ3HHSX3)](https://codecov.io/gh/sigma-epsilon/sigmaepsilon.deepdict)
[![Documentation Status](https://readthedocs.org/projects/sigmaepsilondeepdict/badge/?version=latest)](https://sigmaepsilondeepdict.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://badge.fury.io/py/sigmaepsilon.deepdict.svg)](https://pypi.org/project/sigmaepsilon.deepdict)
[![Python 3.7‒3.10](https://img.shields.io/badge/python-3.7%E2%80%923.10-blue)](https://www.python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Requirements Status](https://dependency-dash.repo-helper.uk/github/sigma-epsilon/sigmaepsilon.deepdict/badge.svg)](https://dependency-dash.repo-helper.uk/github/sigma-epsilon/sigmaepsilon.deepdict)

A Lightweight Python library to manage nested dictionaries with parent-child relationships.
On top of being a compatible drop-in replcement of the build in ``dict`` class, the self replicating default factory makes the creation of complex nested layouts effortless.

## **Documentation**

The [documentation](https://sigmaepsilondeepdict.readthedocs.io/en/latest/) is built with [Sphinx](https://www.sphinx-doc.org/en/master/) using the [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html) and hosted on [ReadTheDocs](https://readthedocs.org/).

## **Installation**

This is optional, but we suggest you to create a dedicated virtual enviroment at all times to avoid conflicts with your other projects. Create a folder, open a command shell in that folder and use the following command

```console
>>> python -m venv venv_name
```

Once the enviroment is created, activate it via typing

```console
>>> .\venv_name\Scripts\activate
```

The library can be installed (either in a virtual enviroment or globally) from PyPI using `pip` on Python >= 3.7:

```console
>>> pip install sigmaepsilon.deepdict
```

## **Usage**

In every case where you'd want to use a `dict`, you can use a `DeepDict` as a drop-in replacement, but on top of what a simple dictionary provides, a `DeepDict` is more capable, as it provides a machinery to handle nested layouts. It is basically an ordered `defaultdict` with a self replicating default factory.

```python
>>> from sigmaepsilon.deepdict import DeepDict
>>> data = DeepDict()
```

A `DeepDict` is essentially a nested default dictionary. Being nested refers to the fact that you can do this:

```python
>>> data['a']['b']['c']['e'] = 1
>>> data['a']['b']['d'] = 2
```

Notice that the object carves a way up until the last key, without needing to create each level explicitly. What happens is that every time a key is missing in a `data`, the object creates a new instance, which then is also ready to handle missing keys or data. Accessing nested subdictionaries works in a similar fashion:

```python
>>> data['a']['b']['c']['e']
1
```

To allow for a more Pythonic feel, it also supports array-like indexing, so that the following operations are valid:

```python
>>> data['a', 'b', 'c', 'e'] = 3
>>> data['a', 'b', 'c', 'e']
3
```

Of course, this is something that we can easily replicate using pure Python in one line, without the need for fancy stuff:

```python
>>> data = {'a' : {'b' : {'c' : {'e' : 3}, 'd' : 2}}}    
```

The key point is that we loop over a pure `dict` instance, we get

```python
>>> [k for k in data.keys()]
['a']    
```

But if we use a `DeepDict` class and the option `deep=True` when accessing
keys, values or items of dictionaries, the following happens:

```python
>>> [k for k in DeepDict(data).keys(deep=True)]
['e', 'd']    
```

We can see, that in this case, iteration goes over keys, that actually hold on to some data, and does not return the containers themselves. If we do the same experiment with the values, it shows that the `DeepDict` only returns the leafs of the data-tree and the behaviour is fundamentally different:

```python
>>> [k for k in data.values()]
[{'b': {'c': {'e': 3}, 'd': 2}}]    
```

```python
>>> [k for k in DeepDict(data).values(deep=True)]
[3, 2]    
```

It is important, that the call `obj.values(deep=True)` still returns a generator object, which makes it memory efficient when looping over large datasets.

```python
>>> DeepDict(data).values(deep=True)
<generator object OrderedDefaultDict.values at 0x0000028F209D54A0>    
```

## **Testing**

To run all tests, open up a console in the root directory of the project and type the following

```console
>>> python -m unittest
```

## **Dependencies**

The only dependency is `six`, to provide basic continuity between major Python versions 2 and 3.

## **License**

This package is licensed under the MIT license.
