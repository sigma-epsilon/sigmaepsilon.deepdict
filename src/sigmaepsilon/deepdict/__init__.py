from os.path import dirname, abspath
from importlib.metadata import metadata

from sigmaepsilon.core.config import namespace_package_name

from .deepdict import DeepDict, Key, Value
from .utils import dictparser, parseaddress, parsedicts, parseitems, parsedicts_addr

__all__ = [
    "DeepDict",
    "Key",
    "Value",
    "dictparser",
    "parseaddress",
    "parseitems",
    "parsedicts",
    "parsedicts_addr",
]

__pkg_name__ = namespace_package_name(dirname(abspath(__file__)), 10)
__pkg_metadata__ = metadata(__pkg_name__)
__version__ = __pkg_metadata__["version"]
__description__ = __pkg_metadata__["summary"]
del __pkg_metadata__
