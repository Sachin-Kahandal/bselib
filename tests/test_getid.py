"""getId.py bridges a BSE script code to MarketsMojo IDs / Screener URLs."""

from __future__ import annotations

from bselib import getId


def test_get_script_url_returns_screener_path_for_valid_code():
    assert getId.getScriptUrl("500325") == "/company/RELIANCE/consolidated/"


def test_get_script_id_returns_marketsmojo_id():
    assert getId.getScript_id("500325", "id") == "605152"


def test_get_script_id_with_non_id_request_returns_trimmed_company_name():
    assert getId.getScript_id("500325", "name") == "Reliance Industries Ltd"


def test_get_script_url_rejects_non_six_digit_code():
    assert getId.getScriptUrl("123") == {"info": "Not a valid script_code"}


def test_get_script_id_rejects_non_six_digit_code():
    assert getId.getScript_id("123", "id") == {"info": "Not a valid script_code"}


def test_get_script_id_returns_error_on_non_numeric_input():
    assert getId.getScript_id("notacode", "id") == {"info": "Error"}
