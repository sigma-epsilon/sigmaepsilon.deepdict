# **SigmaEpsilon.DeepDict** - A lightweight Python library to handle nested dictionaries

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/sigma-epsilon/sigmaepsilon.deepdict/tree/main.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/sigma-epsilon/sigmaepsilon.deepdict/tree/main)
[![codecov](https://codecov.io/gh/sigma-epsilon/sigmaepsilon.deepdict/graph/badge.svg?token=7JKJ3HHSX3)](https://codecov.io/gh/sigma-epsilon/sigmaepsilon.deepdict)
[![Documentation Status](https://readthedocs.org/projects/sigmaepsilondeepdict/badge/?version=latest)](https://sigmaepsilondeepdict.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://badge.fury.io/py/sigmaepsilon.deepdict.svg)](https://pypi.org/project/sigmaepsilon.deepdict)
[![Python 3.7‒3.10](https://img.shields.io/badge/python-3.7%E2%80%923.10-blue)](https://www.python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Requirements Status](https://dependency-dash.repo-helper.uk/github/sigma-epsilon/sigmaepsilon.deepdict/badge.svg)](https://dependency-dash.repo-helper.uk/github/sigma-epsilon/sigmaepsilon.deepdict)

The `DeepDict` class works very similarly to a regular `dict`, but makes life easier in sutiations where there are nested levels, especially when such dictionary is to be created dynamically.

## Motivating examples

Consider the following simple dictionary

```python
>>> d = {
...   "a" : {"aa" : 1},
...   "b" : 2,
...   "c" : {"cc" : {"ccc" : 3}}, 
... }
```

This is what happens when you iterate through the values of it:

```python
>>> list(d.values())
[{'aa': 1}, 2, {'cc': {'ccc': 3}}]
```

If you wrap it as a `DeepDict`:

```python
>>> from sigmaepsilon.deepdict import DeepDict
>>> dd = DeepDict.wrap(d)
>>> list(dd.values(deep=True))
[1, 2, 3]
```

The class supports array-like indexing, which combined with the default factory creates the possibility to create deep levels without having to create all the parents:

```python
>>> data = DeepDict()
>>> data["a", 0, "b", 1, 5] = 10
```

Each subdirectory is aware about it's parent container

```python
>>> data["a", 0, "b"].key
"b"
```

```python
>>> data["a", 0, "b"].address
['a', 0, 'b']
```

```python
>>> data["a", 0, "b"].parent.key
0
```

Given that the `asciitree` library is installed, it is also possible to print dictionaries (any kind) as a tree:

```python
>>> from sigmaepsilon.deepdict import asciiprint
>>> d = {
...     "a" : {"aa" : 1},
...     "b" : 2,
...     "c" : {"cc" : {"ccc" : 3}},
... }
>>> data = DeepDict.wrap(d)
>>> data.name = "Data"
>>> asciiprint(data)
Data
    +-- a
    +-- c
        +-- cc
```

See the documentation for more examples and explanation on behaviour.

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

## **License**

This package is licensed under the [MIT license](LICENSE.txt).
