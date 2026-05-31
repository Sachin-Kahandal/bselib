"""gainers.py — top gainers/losers of the day and NSE/BSE market status."""

from __future__ import annotations

from bselib import gainers

ROW_KEYS = {"securityID", "scriptCode", "LTP", "change", "pChange"}


def test_get_gainers_returns_five_rows_with_expected_shape():
    data = gainers.get_gainers()
    rows = data["gainers"]
    assert len(rows) == 5
    assert all(set(row) == ROW_KEYS for row in rows)


def test_get_gainers_parses_the_top_row():
    top = gainers.get_gainers()["gainers"][0]
    assert top["securityID"] == "SUPRIYA"
    assert top["scriptCode"] == "543434"


def test_get_losers_returns_five_rows_with_expected_shape():
    rows = gainers.get_losers()["losers"]
    assert len(rows) == 5
    assert all(set(row) == ROW_KEYS for row in rows)


def test_get_losers_parses_the_top_row():
    top = gainers.get_losers()["losers"][0]
    assert top["securityID"] == "DELTACORP"
    assert top["scriptCode"] == "532848"


def test_get_index_returns_nse_and_bse_status_tuple():
    nse, _bse = gainers.get_index()
    assert nse["market"] == "Capital Market"
    assert "marketStatus" in nse
