"""The BSE facade delegates to the module functions without altering results."""

from __future__ import annotations

import bselib
from bselib import BSE


def test_bse_is_exported_from_package_root():
    assert bselib.BSE is BSE
    assert isinstance(bselib.__version__, str)


def test_quote_delegates_to_quote_module():
    assert BSE().quote("500325")["stockName"] == "Reliance Industries Ltd"


def test_script_delegates_to_script_module():
    assert BSE().script("500325")[500325] == "Reliance Industries Ltd - 500325"


def test_get_gainers_delegates_to_gainers_module():
    assert len(BSE().get_gainers()["gainers"]) == 5


def test_comp_profile_delegates_to_quote_get_profile():
    assert BSE().comp_profile("500325")["Name"] == "Reliance Industries Ltd"


def test_index_delegates_to_gainers_get_index():
    nse, _bse = BSE().index()
    assert nse["market"] == "Capital Market"


def test_repr_and_str_describe_the_driver():
    assert str(BSE()) == "Driver Class for Bombay Stock Exchange"
    assert repr(BSE()) == "Driver Class for Bombay Stock Exchange"
