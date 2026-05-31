"""Contract tests: pin the upstream structure the parsers depend on.

For every saved fixture we declare the *anchors* the parser relies on — CSS
selectors for HTML pages, top-level keys for JSON endpoints. Two layers:

* offline (default): assert each saved fixture still contains its anchors, so a
  fixture can never silently drift away from what the parser expects.
* live (``-m live``): fetch the real endpoint and assert the same anchors are
  present. A failure here means the upstream site changed its markup/schema and
  the scraper needs updating — exactly the silent rot bselib used to hide.
"""

from __future__ import annotations

import json

import pytest
import requests
from bs4 import BeautifulSoup

from bselib.quote import bse_api_headers, headers

from .conftest import FIXTURES, RELIANCE

# fixture -> CSS selectors the HTML parsers select on
HTML_ANCHORS: dict[str, list[str]] = {
    "bse_stockreach.html": [
        "span.companyname",
        "span.srcovalue strong",
        "td#tdgroup.resultleft",
        "td#tdfacevalue.resultleft",
        "tr#trMktCap td.TTRow_right",
    ],
    "bse_homepage.html": [
        "div#divGainers tr:nth-of-type(2) a.announcelink",
        "div#divLosers tr:nth-of-type(2) a",
    ],
    "screener_company.html": [
        "h1",
        "section#quarters td",
        "section#profit-loss td",
        "section#balance-sheet td",
        "div.annual-reports a",
        "div.pros",
        "div.cons",
    ],
}

# fixture -> top-level JSON keys the parsers read
JSON_ANCHORS: dict[str, list[str]] = {
    "bse_highlow.json": ["Fifty2WkHigh_adj", "Fifty2WkLow_adj", "MonthHighLow"],
    "bse_comheader.json": ["SecurityId"],
    "bse_eqpeergp.json": ["Table"],
}

# fixture -> (live URL, headers) for the live drift check
LIVE_HTML = {
    "bse_stockreach.html": (f"https://m.bseindia.com/StockReach.aspx?scripcd={RELIANCE}", headers),
    "bse_homepage.html": ("https://m.bseindia.com", headers),
    "screener_company.html": ("https://www.screener.in/company/RELIANCE/consolidated/", headers),
}
LIVE_JSON = {
    "bse_highlow.json": (
        f"https://api.bseindia.com/BseIndiaAPI/api/HighLow/w?Type=EQ&flag=C&scripcode={RELIANCE}",
        bse_api_headers,
    ),
    "bse_comheader.json": (
        f"https://api.bseindia.com/BseIndiaAPI/api/ComHeader/w?quotetype=EQ&scripcode={RELIANCE}&seriesid=",
        bse_api_headers,
    ),
    "bse_eqpeergp.json": (
        f"https://api.bseindia.com/BseIndiaAPI/api/EQPeerGp/w?scripcode={RELIANCE}&scripcomare=",
        bse_api_headers,
    ),
}


def _missing_selectors(html: str, selectors: list[str]) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    return [sel for sel in selectors if not soup.select(sel)]


def _missing_keys(payload: object, keys: list[str]) -> list[str]:
    assert isinstance(payload, dict), f"expected a JSON object, got {type(payload).__name__}"
    return [k for k in keys if k not in payload]


def _fetch(url: str, hdrs: dict[str, str]) -> requests.Response:
    try:
        return requests.get(url, headers=hdrs, timeout=30)
    except requests.RequestException as exc:  # network down / blocked — not a drift
        pytest.skip(f"live endpoint unreachable: {exc}")


# --- offline: fixtures keep their anchors -------------------------------------


@pytest.mark.parametrize("fixture", HTML_ANCHORS)
def test_html_fixture_contains_parser_anchors(fixture: str):
    missing = _missing_selectors((FIXTURES / fixture).read_text(), HTML_ANCHORS[fixture])
    assert not missing, f"{fixture} fixture lost selectors: {missing}"


@pytest.mark.parametrize("fixture", JSON_ANCHORS)
def test_json_fixture_contains_parser_anchors(fixture: str):
    payload = json.loads((FIXTURES / fixture).read_text())
    assert not _missing_keys(payload, JSON_ANCHORS[fixture])


# --- live: real upstream still matches the fixture anchors --------------------


@pytest.mark.live
@pytest.mark.parametrize("fixture", LIVE_HTML)
def test_live_html_structure_has_not_drifted(fixture: str):
    url, hdrs = LIVE_HTML[fixture]
    missing = _missing_selectors(_fetch(url, hdrs).text, HTML_ANCHORS[fixture])
    assert not missing, f"upstream for {fixture} dropped selectors: {missing} (update the scraper)"


@pytest.mark.live
@pytest.mark.parametrize("fixture", LIVE_JSON)
def test_live_json_schema_has_not_drifted(fixture: str):
    url, hdrs = LIVE_JSON[fixture]
    missing = _missing_keys(_fetch(url, hdrs).json(), JSON_ANCHORS[fixture])
    assert not missing, f"upstream for {fixture} dropped keys: {missing} (update the scraper)"
