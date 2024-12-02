# Changelog

All notable changes to this project will be documented in this file. If you are interested in bug fixes, enhancements etc., best follow the project on GitHub.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Additionally, this changelog includes a "Refactored" section for changes that do not modify the behavior of the code.

## [Unreleased]

### Changed

The following behavior has been changed:

```python
from sigmaepsilon.deepdict import DeepDict
dd = DeepDict()
dd["key"] = "value"
dd["key"] = None
```

Previously, this would delete the key from the dictionary, which was inconsistent with the behavior of the built-in `dict` class. Starting from this version, the last line will only set the value to `None` without deleting the key. To delete the key, you should now use:

```python
del dd["key"]
```

### Refactored

Refactored the implementations of magic methods `__setitem__`, `__getitem__` and `__delitem__` for better clarity and improved code quality.

## [2.0.0] - 2023-10-01

### Changed

The generic types of the `DeepDict` class have been changed. Now it accepts types as the built-in `dict` type.

## [1.1.0] - 2023-10-01

### Added

- Helper classes for Keys and Values to make it possible to bypass behaviour.

### Fixed

- Issue of tuple keys. It was not possible to define subdictionaries with tuple keys. Now
  it is possible with the provided `Key` helper class.

### Changed

### Removed
