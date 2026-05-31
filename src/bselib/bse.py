from __future__ import annotations

from typing import Any

from bselib import analysis, gainers, quote, script, statements


class BSE:
    """Facade exposing every bselib feature through one stateless object.

    Each method delegates to a module-level function. Errors are returned as
    sentinel dicts (e.g. ``{'info': 'Error'}``), never raised.
    """

    def analysis(self, script_code: int | str) -> dict[str, Any] | tuple[Any, Any]:
        """Return analysis of price and value for a script."""
        return analysis.analysis(script_code)

    def stmt_analysis(self, script_code: int | str, stats: str) -> dict[str, Any] | tuple[Any, Any]:
        """Return analysis of financial statements."""
        return analysis.stmt_analysis(script_code, stats)

    def corporate_actions(self, script_code: int | str) -> dict[str, Any]:
        """Return board meetings, dividends, splits, bonus and rights issued."""
        return quote.corporate_actions(script_code)

    def get_gainers(self) -> dict[str, Any]:
        """Return the top 5 performers of the day."""
        return gainers.get_gainers()

    def holdings(self, script_code: int | str) -> dict[str, Any]:
        """Return the shareholding pattern and analysis."""
        return quote.holdings(script_code)

    def index(self) -> tuple[Any, Any]:
        """Return NSE and BSE basic market status."""
        return gainers.get_index()

    def get_losers(self) -> dict[str, Any]:
        """Return the worst 5 performers of the day."""
        return gainers.get_losers()

    def news(self, script_code: int | str) -> dict[str, Any]:
        """Return news related to a company."""
        return quote.news(script_code)

    def peers(self, script_code: int | str) -> dict[str, Any]:
        """Return competitors and some info within the same sector."""
        return quote.peers(script_code)

    def comp_profile(self, script_code: int | str) -> dict[str, Any]:
        """Return information about a company's business."""
        return quote.get_profile(script_code)

    def script(self, stock: int | str) -> dict[str, Any]:
        """Return script codes for a searched stock."""
        return script.script(stock)

    def quote(self, script_code: int | str) -> dict[str, Any]:
        """Return basic details: current price, market cap, highs/lows and bulk deals."""
        return quote.quote(script_code)

    def bulk_deals(self, script_code: int | str) -> dict[str, Any]:
        """Return bulk deals for a script."""
        return quote.bulk_deals(script_code)

    def ratios(self, script_code: int | str) -> dict[str, Any]:
        """Return a few key financial ratios."""
        return quote.ratios(script_code)

    def statement(self, script_code: int | str, stats: str) -> dict[str, Any]:
        """Return a snapshot of recent financial statements."""
        return statements.statement(script_code, stats)

    def historical_stats(self, script_code: int | str, stats: str) -> dict[str, Any]:
        """Return snapshots of historical financial statements."""
        return statements.historical_stats(script_code, stats)

    def annual_reports(self, script_code: int | str) -> dict[str, Any]:
        """Return links to annual reports."""
        return statements.annual_reports(script_code)

    def credit_reports(self, script_code: int | str) -> dict[str, Any]:
        """Return links to credit reports."""
        return statements.credit_reports(script_code)

    def __str__(self) -> str:
        return "Driver Class for Bombay Stock Exchange"

    def __repr__(self) -> str:
        return "Driver Class for Bombay Stock Exchange"
