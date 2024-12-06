# Changelog

All notable changes to this project will be documented in this file. If you are interested in bug fixes, enhancements etc., best follow the project on GitHub.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Additionally, this changelog includes a "Refactored" section for changes that do not modify the behavior of the code.

## [XXX.YYY.ZZZ] - [Unreleased]

## [3.0.0] - 2024-12-06

### Added

- Added type checks for the magic methods ``__getitem__``, ``__setitem__`` and ``__delitem__``.
- Added a custom exception type ``DeepDictLockedError`` for when a locked dictionary is about to be modified.
- Added new special methods `__before_join_parent__`, `__after_join_parent__`, `__before_leave_parent__` and `__after_leave_parent__` to replace the hooks `__leave_parent__` and `__join_parent__`.

### Changed

- The behaviour when assigning a `None` value to a key has been changed:

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

- Customizing the behaviour upon deleting a DeepDict from its parent and adding a child DeepDict has been changed, see the notes at the 'Deprecated' section.

- Changed the locking behaviour to cover for all scenarios that would modify the layout of a dictionary. The previous implementation only covered creating new keys, but it didn't protect agains deletions.

### Deprecated

The use of the hooks `__leave_parent__` and `__join_parent__` is deprecated. They are replaced with `__before_join_parent__`, `__after_join_parent__`, `__before_leave_parent__` and `__after_leave_parent__`, which provides more fine grained control. See the documentation for more details.

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
