"""analysis.py — fundamental analysis, pros/cons, statement analysis."""

from __future__ import annotations

from bselib import analysis


def test_analysis_combines_value_price_and_pros_cons():
    data = analysis.analysis("500325")
    assert set(data) == {"value_analysis", "price_analysis", "pros", "cons"}
    assert {"quality", "valuation", "technicals"} <= set(data["value_analysis"])


def test_analysis_parses_pros_and_cons_as_bullet_lists():
    data = analysis.analysis("500325")
    assert isinstance(data["pros"], list)
    assert isinstance(data["cons"], list)
    # Reliance currently has cons listed on Screener; pros may be empty.
    assert any("return on equity" in c for c in data["cons"])


def test_stmt_analysis_quarter_results_returns_qoq_and_yoy_tuple():
    result = analysis.stmt_analysis("500325", "quarter_results")
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_stmt_analysis_balancesheet_wraps_under_bal_analysis():
    result = analysis.stmt_analysis("500325", "balancesheet")
    assert "bal_analysis" in result


def test_stmt_analysis_rejects_unknown_statement_type():
    assert "error" in analysis.stmt_analysis("500325", "nonsense")
