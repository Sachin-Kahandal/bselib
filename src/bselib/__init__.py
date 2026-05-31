"""bselib — scrape and aggregate real-time and historical BSE / Indian market data.

Everything is reached through the :class:`~bselib.bse.BSE` facade::

    from bselib import BSE

    bse = BSE()
    bse.quote("500325")
"""

from importlib.metadata import PackageNotFoundError, version

from bselib.bse import BSE

try:
    __version__ = version("bselib")
except PackageNotFoundError:  # package is not installed (e.g. running from a source tree)
    __version__ = "0.0.0"

__all__ = ["BSE", "__version__"]
