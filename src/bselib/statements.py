from __future__ import annotations

from typing import Any, cast

import requests
from bs4 import BeautifulSoup
from pandas import read_html

from bselib.getId import getScriptUrl

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
}
baseurl = "https://www.screener.in"
invalid_script_code = {"info": "Not a valid script_code"}
error = {"info": "Error"}


def historical_stats(script_code: int | str, stats: str) -> dict[str, Any]:
    screener_url = getScriptUrl(script_code)
    try:
        df = read_html(baseurl + str(screener_url), index_col=None)
        # QUARTERLY RESULTS
        if stats == "quarter_results":
            return cast("dict[str, Any]", df[0].to_dict())
        # PROFIT-LOSS STATEMENTS
        elif stats == "yoy_results":
            return cast("dict[str, Any]", df[1].to_dict())
        # BALANCESHEETS
        elif stats == "balancesheet":
            return cast("dict[str, Any]", df[6].to_dict())
        # CASHFLOW
        elif stats == "cashflow":
            return cast("dict[str, Any]", df[7].to_dict())
        else:
            return {
                "error": "select either of these statements: cashflow, yoy_results, quarter_results, balancesheet"
            }
    except Exception:
        return error


def statement(script_code: int | str, stats: str) -> dict[str, Any]:
    screener_url = getScriptUrl(script_code)
    try:
        res = requests.get(baseurl + str(screener_url), headers=headers)
        soup = BeautifulSoup(res.text, "lxml")
        head = [
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
        ]
        item = []
        #  quarter results
        if stats == "quarter_results":
            latest_qrt = soup.select("section#quarters td:nth-of-type(8)")
            for i in range(0, len(head)):
                item.append(latest_qrt[i].text)

            qrt_res = dict(zip(head, item))
            return qrt_res

        #  ttm results
        elif stats == "ttm_results":
            ttm_pl = soup.select("section#profit-loss td:nth-of-type(12)")
            for i in range(0, len(head)):
                item.append(ttm_pl[i].text)

            pl_ttm = dict(zip(head, item))
            return pl_ttm

        # yoy results
        elif stats == "yoy_results":
            yoy_pl = soup.select("section#profit-loss td:nth-of-type(11)")
            for i in range(0, len(head)):
                item.append(yoy_pl[i].text)

            pl_yoy = dict(zip(head, item))
            return pl_yoy

        # balancesheet statement
        elif stats == "balancesheet":
            yoy_bal = soup.select("section#balance-sheet td:nth-of-type(12)")
            head = [
                "share_capital",
                "reserves",
                "borrowings",
                "other_liabilities",
                "total_liabilities",
                "fixed_assets",
                "CWIP",
                "investments",
                "other_assets",
                "total_assets",
            ]
            for i in range(0, len(head)):
                item.append(yoy_bal[i].text)

            yoy_bal_sheet = dict(zip(head, item))
            return yoy_bal_sheet

        # cashflow statement
        elif stats == "cashflow":
            yoy_cf = soup.select("section#cash-flow td:nth-of-type(11)")
            head = [
                "Cash from operating activity",
                "Cash from investing activity",
                "Cash from finance activity",
            ]
            for i in range(0, len(head)):
                item.append(yoy_cf[i].text)

            cf_yoy = dict(zip(head, item))
            return cf_yoy
        else:
            return {
                "info": "select either of these statements: cashflow, yoy_results, quarter_results, balancesheet"
            }
    except Exception:
        return error


def _report_links(soup: BeautifulSoup, css: str) -> dict[str, str]:
    # Collect {visible text: href} for real document anchors under a Screener
    # documents sub-section (skips "View all"/button-style links with no href).
    link_text, links = [], []
    for link in soup.select(css):
        href = link.get("href")
        # bs4 may return a list for multi-valued attrs; only plain http(s) hrefs qualify.
        if not isinstance(href, str) or not href.startswith("http"):
            continue
        text = " ".join(link.get_text().split())
        link_text.append(text)
        links.append(href)
    return dict(zip(link_text, links))


def annual_reports(script_code: int | str) -> dict[str, Any]:
    try:
        screener_url = getScriptUrl(script_code)
        res = requests.get(baseurl + str(screener_url), headers=headers)
        soup = BeautifulSoup(res.content, "lxml")
        # ANNUAL REPORT LINKS (Screener "Documents > Annual reports" section)
        return _report_links(soup, "div.annual-reports a")
    except Exception:
        return error


def credit_reports(script_code: int | str) -> dict[str, Any]:
    try:
        screener_url = getScriptUrl(script_code)
        res = requests.get(baseurl + str(screener_url), headers=headers)
        soup = BeautifulSoup(res.content, "lxml")
        # CREDIT-RATINGS REPORT LINKS (Screener "Documents > Credit ratings" section)
        return _report_links(soup, "div.credit-ratings a")
    except Exception:
        return error
