"""D3 contract: upstream failures are returned as sentinel dicts, never raised."""

from __future__ import annotations

import pytest
import requests

from bselib import analysis, getId, quote, statements

ERROR = {"info": "Error"}


@pytest.fixture
def network_down(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make every requests.get raise, simulating a dead/blocked upstream."""

    def boom(*args: object, **kwargs: object):
        raise requests.ConnectionError("simulated outage")

    monkeypatch.setattr(requests, "get", boom)


@pytest.mark.parametrize(
    "call",
    [
        lambda: quote.quote("500325"),
        lambda: quote.bulk_deals("500325"),
        lambda: quote.ratios("500325"),
        lambda: quote.peers("500325"),
        lambda: quote.holdings("500325"),
        lambda: quote.news("500325"),
        lambda: quote.corporate_actions("500325"),
        lambda: quote.get_profile("500325"),
        lambda: analysis.analysis("500325"),
        lambda: statements.annual_reports("500325"),
        lambda: statements.credit_reports("500325"),
        lambda: getId.getScriptUrl("500325"),
        lambda: getId.getScript_id("500325", "id"),
    ],
)
def test_function_returns_error_sentinel_when_network_is_down(network_down, call):
    assert call() == ERROR


def test_statement_returns_error_sentinel_when_network_is_down(network_down):
    # statement() resolves the Screener URL first; that failing yields the sentinel.
    assert statements.statement("500325", "quarter_results") == ERROR
