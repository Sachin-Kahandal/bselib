"""quote.py — live quotes, ratios, bulk deals, holdings, news, actions, profile."""

from __future__ import annotations

from bselib import quote

INVALID = {"info": "Not a valid script_code"}
ERROR = {"info": "Error"}


def test_quote_parses_core_fields_from_bse_stockreach():
    q = quote.quote("500325")
    assert q["stockName"] == "Reliance Industries Ltd"
    assert q["currentPrice"] == "1320.55"
    assert q["securityId"] == "RELIANCE"
    assert q["scriptCode"] == "500325"
    assert q["group"] == "A"
    assert q["index"] == "BSE SENSEX"
    assert q["faceValue"] == "10.00"


def test_quote_derives_signed_change_from_the_number():
    q = quote.quote("500325")
    assert q["change"] == "-29.45"
    assert q["pChange"] == "-2.18"


def test_quote_merges_highlow_api_into_floats():
    q = quote.quote("500325")
    assert q["fiftytwo_WeekHigh"] == 1611.20
    assert q["fiftytwo_WeekLow"] == 1290.00
    assert q["monthHighLow"] == "1473.65 / 1313.50"


def test_quote_wraps_unit_bearing_values_in_nested_dicts():
    q = quote.quote("500325")
    assert q["mktCap"]["in"] == "Cr"
    assert q["totalTradedValue"]["in"] == "Cr"
    assert "value" in q["mktCap"]


def test_quote_rejects_non_six_digit_code():
    assert quote.quote("123") == INVALID


def test_quote_returns_error_on_non_numeric_code():
    assert quote.quote("abc") == ERROR


def test_bulk_deals_wraps_response_under_bulk_deals_key():
    assert "bulk_deals" in quote.bulk_deals("500325")


def test_bulk_deals_rejects_non_six_digit_code():
    assert quote.bulk_deals("1") == INVALID


def test_ratios_splits_value_and_profit_ratios():
    r = quote.ratios("500325")
    assert r["value_ratio"]["SecurityId"] == "RELIANCE"
    assert set(r["profit_ratio"]) == {"OPM", "NPM", "RONW", "EPS", "CEPS", "PE"}


def test_peers_returns_table():
    assert "Table" in quote.peers("500325")


def test_holdings_exposes_snapshot_compare_and_analysis():
    h = quote.holdings("500325")
    assert set(h) == {"holdings", "holding_comp", "holding_analysis"}


def test_news_wraps_under_news_key():
    assert "news" in quote.news("500325")


def test_corporate_actions_groups_the_five_action_types():
    a = quote.corporate_actions("500325")
    assert set(a) == {"board_meetings", "dividends", "splits", "bonus", "rights"}
    assert len(a["board_meetings"]) <= 3


def test_get_profile_from_screener():
    p = quote.get_profile("500325")
    assert p["script_code"] == 500325
    assert p["Name"] == "Reliance Industries Ltd"
    assert p["website"].startswith("http")
    assert set(p) >= {"description", "bse_link", "nse_link"}


def test_get_profile_rejects_non_six_digit_code():
    assert quote.get_profile("12") == INVALID
