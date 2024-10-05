# **SigmaEpsilon.DeepDict** - A lightweight Python library to handle nested dictionaries

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/sigma-epsilon/sigmaepsilon.deepdict/tree/main.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/sigma-epsilon/sigmaepsilon.deepdict/tree/main)
[![codecov](https://codecov.io/gh/sigma-epsilon/sigmaepsilon.deepdict/graph/badge.svg?token=7JKJ3HHSX3)](https://codecov.io/gh/sigma-epsilon/sigmaepsilon.deepdict)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/077f95d06b9d4ee88395d5c088e4496a)](https://app.codacy.com/gh/sigma-epsilon/sigmaepsilon.deepdict/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Documentation Status](https://readthedocs.org/projects/sigmaepsilondeepdict/badge/?version=latest)](https://sigmaepsilondeepdict.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://badge.fury.io/py/sigmaepsilon.deepdict.svg)](https://pypi.org/project/sigmaepsilon.deepdict)
[![Python](https://img.shields.io/badge/python-3.10|3.11|3.12-blue)](https://www.python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Requirements Status](https://dependency-dash.repo-helper.uk/github/sigma-epsilon/sigmaepsilon.deepdict/badge.svg)](https://dependency-dash.repo-helper.uk/github/sigma-epsilon/sigmaepsilon.deepdict)

`sigmaepsilon.deepdict` is a lightweight Python library designed to handle nested dictionaries more easily, especially in cases where dictionaries are created dynamically. Its key feature is the `DeepDict` class, which extends the regular dict to support nested layouts. It allows easy manipulation of deeply nested structures, array-like indexing, and automatic creation of deep dictionary levels without manually defining all parent keys. It is particularly useful in scenarios involving hierarchical data. The library also supports printing dictionaries as trees.

## Highlights

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

The class allows array-like indexing, and when combined with the default factory, enables the creation of deep levels without manually defining all parent keys:

```python
>>> data = DeepDict()
>>> data["a", 0, "b", 1, 5] = 10
```

Each subdirectory is aware about its parent container

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

The library can be installed from PyPI using `pip` on Python >= 3.10:

```console
>>> pip install sigmaepsilon.deepdict
```

## **License**

This package is licensed under the [MIT license](LICENSE.txt).
