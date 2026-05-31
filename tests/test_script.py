"""script.py — search a stock by name/code -> {script_code: name}."""

from __future__ import annotations

from bselib import script


def test_script_maps_code_to_company_name():
    result = script.script("500325")
    assert result[500325] == "Reliance Industries Ltd - 500325"
