from pathlib import Path

from .session import FlarumUser
from .error_handler import FlarumError

from .flarum.core.discussions import Discussion

from .flarum.core.filters import Filter


__all__ = ['FlarumUser', 'FlarumError', 'Discussion', 'Filter']


__description__ = "An unofficial Python package for manipulating with Flarum's API"
__author__      = "SKevo"
__copyright__   = "Copyright 2021, SKevo"
__credits__     = ["SKevo"]
__license__     = "GPLv3"
__version__     = "v1.0.8-beta"
__maintainer__  = "SKevo"
__email__       = "me@kevo.link"
__status__      = "4 - Beta"

# Default readme:
__readme__ = "(c) SKevo"

# Overwrite docstring, so pdoc can render it:
try:
    with open(f"{Path(__file__).parent.parent.absolute()}{Path('/README.md')}", 'r', encoding="UTF-8") as readme:
        __readme__ = readme.read()

except:
    pass

__doc__ = __readme__
