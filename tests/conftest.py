"""Shared test fixtures.

Unit tests are offline by default: an autouse fixture swaps ``requests.get``
for a router that replays per-endpoint responses saved under ``tests/fixtures``
(captured live from the real upstreams for Reliance, script code 500325).

Tests marked ``@pytest.mark.live`` skip the mock and hit the real endpoints.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import requests

FIXTURES = Path(__file__).parent / "fixtures"
RELIANCE = "500325"
RELIANCE_MOJO_ID = "605152"

# Routing table: the first (substring, fixture) whose substring is in the URL wins.
# Order matters — more specific paths must precede the bare-host catch-alls.
ROUTES: list[tuple[str, str]] = [
    ("StockReach.aspx", "bse_stockreach.html"),
    ("api/HighLow", "bse_highlow.json"),
    ("api/ComHeader", "bse_comheader.json"),
    ("api/EQPeerGp", "bse_eqpeergp.json"),
    ("api/TabResults", "bse_bulkdeals.json"),
    ("Sensex/getSensexData", "bse_sensex.json"),
    ("screener.in/api/company/search", "screener_search.json"),
    ("screener.in/company", "screener_company.html"),
    ("Stocks_Shareholding", "mojo_shareholding.json"),
    ("Stocks_Priceupdates", "mojo_news.json"),
    ("Stocks_Corporateactions", "mojo_corpactions.json"),
    ("stocks_stocksid/header_info", "mojo_headerinfo.json"),
    ("stocks_dashboard/stockinfo", "mojo_stockinfo.json"),
    ("Stocks_Balancesheet", "mojo_balancesheet.json"),
    ("Stocks_Periodicresults", "mojo_periodic_q.json"),
    ("frontendsearch", "mojo_search.txt"),
    ("nseindia.com/api/marketStatus", "nse_marketstatus.json"),
    ("m.bseindia.com", "bse_homepage.html"),
]


def load(name: str) -> str:
    return (FIXTURES / name).read_text()


def fixture_for(url: str) -> str:
    for substring, name in ROUTES:
        if substring in url:
            return name
    raise AssertionError(f"No fixture mapped for URL: {url}")


class FakeResponse:
    """Minimal stand-in for ``requests.Response`` covering what bselib reads."""

    def __init__(self, body: str, status: int = 200) -> None:
        self.text = body
        self.content = body.encode("utf-8")
        self.status_code = status
        self.headers = {"content-type": "application/json"}

    def json(self) -> object:
        return json.loads(self.text)


def fake_get(url: str, *args: object, **kwargs: object) -> FakeResponse:
    return FakeResponse(load(fixture_for(url)))


@pytest.fixture(autouse=True)
def _http(request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch) -> None:
    """Replay saved fixtures for ``requests.get`` unless the test is marked ``live``."""
    if request.node.get_closest_marker("live"):
        return  # hit the real network
    monkeypatch.setattr(requests, "get", fake_get)
