# **SigmaEpsilon.DeepDict** - A lightweight Python library for nested dictionaries

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/sigma-epsilon/sigmaepsilon.deepdict/tree/main.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/sigma-epsilon/sigmaepsilon.deepdict/tree/main)
[![codecov](https://codecov.io/gh/sigma-epsilon/sigmaepsilon.deepdict/graph/badge.svg?token=7JKJ3HHSX3)](https://codecov.io/gh/sigma-epsilon/sigmaepsilon.deepdict)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/077f95d06b9d4ee88395d5c088e4496a)](https://app.codacy.com/gh/sigma-epsilon/sigmaepsilon.deepdict/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Documentation Status](https://readthedocs.org/projects/sigmaepsilondeepdict/badge/?version=latest)](https://sigmaepsilondeepdict.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/sigmaepsilon.deepdict)](https://pypi.org/project/sigmaepsilon.deepdict)
[![PyPI - Version](https://img.shields.io/pypi/v/sigmaepsilon.deepdict)](https://pypi.org/project/sigmaepsilon.deepdict)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sigmaepsilon.deepdict)](https://www.python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Static Badge](https://img.shields.io/badge/versioning-semver-orange)](https://semver.org/)

`sigmaepsilon.deepdict` is a lightweight Python library designed to handle nested dictionaries more easily, especially in cases where dictionaries are created dynamically. Its key feature is the `DeepDict` class, which extends the regular dict to support nested layouts. It allows easy manipulation of deeply nested structures, array-like indexing, and automatic creation of deep dictionary levels without manually defining all parent keys. It is particularly useful in scenarios involving hierarchical data. The library also supports printing dictionaries as trees.

The first implementation of the `DeepDict` class was based on [this](http://stackoverflow.com/a/6190500/562769) StackOverflow thread.

## Key Features

- **Nested Layout Support**: DeepDict allows for seamless manipulation of deeply nested structures, enabling array-like indexing and automatic creation of nested dictionary levels without the need to manually define all parent keys.

- **Parent-Child Awareness**: Each sub-dictionary within a DeepDict is aware of its parent container, providing attributes like key, address, and parent.key to facilitate navigation and management of the nested structure.

- **Tree Representation**: With the optional installation of the asciitree library, DeepDict can print dictionaries as trees, offering a visual representation of the nested data.

## Example Usage

```python
from sigmaepsilon.deepdict import DeepDict

# Creating a DeepDict instance
data = DeepDict()
data["a", 0, "b", 1, 5] = 10

# Accessing attributes
print(data["a", 0, "b"].key)       # Output: 'b'
print(data["a", 0, "b"].address)   # Output: ['a', 0, 'b']
print(data["a", 0, "b"].parent.key) # Output: 0

```

See the documentation for more examples and explanation on behaviour.

## **Documentation**

The [documentation](https://sigmaepsilondeepdict.readthedocs.io/en/latest/) is built with [Sphinx](https://www.sphinx-doc.org/en/master/) using the [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/en/stable/index.html) and hosted on [ReadTheDocs](https://readthedocs.org/).

## **Installation**

For installation instructions, please refer to the [documentation](https://sigmaepsilondeepdict.readthedocs.io/en/latest/).

## **License**

This package is licensed under the [MIT license](LICENSE.txt).
