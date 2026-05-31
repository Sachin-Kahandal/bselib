# bselib

[![CI](https://github.com/Sachin-Kahandal/bselib/actions/workflows/ci.yml/badge.svg)](https://github.com/Sachin-Kahandal/bselib/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Sachin-Kahandal/bselib/branch/master/graph/badge.svg)](https://codecov.io/gh/Sachin-Kahandal/bselib)
[![PyPI version](https://img.shields.io/pypi/v/bselib.svg)](https://pypi.org/project/bselib/)
[![Python versions](https://img.shields.io/pypi/pyversions/bselib.svg)](https://pypi.org/project/bselib/)
[![License: MIT](https://img.shields.io/pypi/l/bselib.svg)](LICENSE)

Python library for extracting real-time and historical data for stocks listed on the
Bombay Stock Exchange (India).

## Introduction

bselib collects real-time data from the Bombay Stock Exchange and historical data from a few
other sources. It can be used in projects that need live quotes, historical data, corporate
news and actions, ratios, financial statements, credit reports and analysis — stock
simulators and portfolio managers, for example.

Quotes are only as accurate as the [BSE website](https://www.bseindia.com).

> **Please do not use this library for production usage.** It is best used for learning and
> building applications for your own use. For commercial applications, buy a data service.
>
> This library uses the MIT license, so liability lies with the user, not the author.

## Installation

```bash
pip install bselib
```

bselib supports Python 3.9+.

## Quickstart

Everything is reached through the `BSE` facade:

```python
from bselib import BSE

bse = BSE()

# Live quote by 6-digit BSE script code (Reliance = 500325)
bse.quote("500325")
# {'stockName': 'Reliance Industries Ltd', 'currentPrice': '1320.55', ...}

# Search for a stock's script code
bse.script("reliance")
# {500325: 'Reliance Industries Ltd - 500325', ...}

# Top gainers / losers of the day
bse.get_gainers()
bse.get_losers()

# Fundamentals
bse.ratios("500325")
bse.statement("500325", "quarter_results")
bse.holdings("500325")
bse.comp_profile("500325")
```

Errors are returned as sentinel dicts, never raised — so a quick call never needs a
`try/except`:

```python
bse.quote("123")     # {'info': 'Not a valid script_code'}
bse.quote("abc")     # {'info': 'Error'}
```

## Features

* Live quotes by script code, and script-code lookup by search.
* Top gainers and losers of the day; NSE/BSE market status.
* Financial statements: quarterly results, profit & loss, balance sheets, cash flows
  (latest snapshot and historical).
* Statement analysis, key ratios, and company fundamentals.
* Corporate actions: board meetings, dividends, bonus, splits and rights.
* Links to annual reports and credit-rating reports.
* Shareholding patterns, peer comparisons, news and pros/cons analysis.

## API

| Method | Returns |
|---|---|
| `quote(script_code)` | Live price, market cap, highs/lows |
| `script(stock)` | `{script_code: name}` matches for a search |
| `ratios(script_code)` | Key value & profitability ratios |
| `bulk_deals(script_code)` | Bulk deals |
| `peers(script_code)` | Peer comparison |
| `holdings(script_code)` | Shareholding pattern & analysis |
| `news(script_code)` | Company news |
| `corporate_actions(script_code)` | Board meetings, dividends, splits, bonus, rights |
| `comp_profile(script_code)` | Business profile |
| `statement(script_code, stats)` | Latest financial statement snapshot |
| `historical_stats(script_code, stats)` | Historical statements |
| `stmt_analysis(script_code, stats)` | Statement analysis |
| `analysis(script_code)` | Price/value analysis + pros/cons |
| `annual_reports(script_code)` / `credit_reports(script_code)` | Document links |
| `get_gainers()` / `get_losers()` / `index()` | Market movers & status |

`stats` is one of `quarter_results`, `yoy_results`, `balancesheet`, `cashflow`
(plus `ttm_results` for `statement`, `profitloss` for `stmt_analysis`).

Full docs: https://bselib.readthedocs.io/en/latest/

## Architecture

bselib is a thin, stateless facade over several upstream sources (BSE, Screener.in,
MarketsMojo, NSE), picking the best free source per data type. The rationale for every
design choice lives in [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md).

## Development

This project uses [uv](https://docs.astral.sh/uv/).

```bash
uv sync                       # create the env and install dev dependencies
uv run pytest                 # offline tests (replayed fixtures, no network)
uv run pytest -m live         # contract tests against the real upstreams
uv run ruff check .           # lint
uv run ruff format .          # format
uv run mypy                   # type-check
uvx pre-commit install        # run the checks on every commit
```

## Dependencies

* [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Requests](https://requests.readthedocs.io/)
* [pandas](https://pandas.pydata.org/)
* [html5lib](https://html5lib.readthedocs.io/) and [lxml](https://lxml.de/)
* A working internet connection.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2020 Sachin Kahandal.
