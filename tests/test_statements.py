"""statements.py — financial statements (HTML + pandas) and report links."""

from __future__ import annotations

import pandas as pd
import pytest

from bselib import statements

from .conftest import FIXTURES

QUARTER_KEYS = {
    "sales",
    "expenses",
    "operating_profit",
    "opm",
    "other_income",
    "interest",
    "depreciation",
    "profit_before_tax",
    "tax_percentage",
    "net_profit",
    "eps",
}


def test_statement_quarter_results_has_all_line_items():
    stmt = statements.statement("500325", "quarter_results")
    assert set(stmt) == QUARTER_KEYS
    assert "231,535" in stmt["sales"]


def test_statement_balancesheet_uses_balancesheet_line_items():
    stmt = statements.statement("500325", "balancesheet")
    assert "total_assets" in stmt
    assert "share_capital" in stmt


def test_statement_rejects_unknown_statement_type():
    assert "info" in statements.statement("500325", "nonsense")


def test_annual_reports_returns_text_to_http_url_mapping():
    reports = statements.annual_reports("500325")
    assert reports
    assert all(url.startswith("http") for url in reports.values())


def test_credit_reports_returns_text_to_http_url_mapping():
    reports = statements.credit_reports("500325")
    assert reports
    assert all(url.startswith("http") for url in reports.values())


def test_historical_stats_quarter_results(monkeypatch: pytest.MonkeyPatch):
    # historical_stats uses pandas.read_html (not requests), so mock it directly.
    monkeypatch.setattr(
        statements,
        "read_html",
        lambda *a, **k: pd.read_html(FIXTURES / "screener_company.html"),
    )
    result = statements.historical_stats("500325", "quarter_results")
    assert isinstance(result, dict)
    assert len(result) > 1


def test_historical_stats_rejects_unknown_statement_type(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        statements,
        "read_html",
        lambda *a, **k: pd.read_html(FIXTURES / "screener_company.html"),
    )
    assert "error" in statements.historical_stats("500325", "nonsense")
