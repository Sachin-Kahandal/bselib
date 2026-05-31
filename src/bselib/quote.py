from __future__ import annotations

from typing import Any

import requests
from bs4 import BeautifulSoup

from bselib.getId import getScript_id, getScriptUrl

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
}
# api.bseindia.com now rejects requests that don't originate from the BSE site:
# without these Origin/Referer headers it serves the SPA landing page (HTML) instead
# of JSON, so .json() fails. Required for HighLow / TabResults / ComHeader / EQPeerGp.
bse_api_headers = dict(
    headers,
    **{
        "Origin": "https://www.bseindia.com",
        "Referer": "https://www.bseindia.com/",
        "Accept": "application/json, text/plain, */*",
    },
)
invalid_script_code = {"info": "Not a valid script_code"}
error = {"info": "Error"}


def quote(script_code: int | str) -> dict[str, Any]:
    try:
        # script codes are suppose to be 6 digit integers
        script_code = int(script_code)
        if len(str(script_code)) == 6:
            baseurl = "https://m.bseindia.com/StockReach.aspx?scripcd="
            response = requests.get(baseurl + str(script_code), headers=headers)
            soup = BeautifulSoup(response.text, "lxml")
            quote = {}
            quote["stockName"] = soup.select("span.companyname")[0].text
            if quote["stockName"] != "":
                quote["currentPrice"] = soup.select("span.srcovalue strong")[0].text
                try:
                    # e.g. "-29.45 ( -2.18%)" — BSE already encodes the sign, so derive
                    # the prefix from the number itself instead of string-comparing prices.
                    change_text = soup.select("span#spanchangVal.srcovalue")[0].text
                    change = change_text.split("(")[0].strip().replace("+", "")
                    pChange = change_text.split("(")[1].strip()[:-2].replace("+", "")
                    sign = "+" if float(change.replace(",", "")) > 0 else ""
                    quote["change"] = sign + change
                    quote["pChange"] = sign + pChange
                except (IndexError, ValueError):
                    quote["change"] = "-"
                    quote["pChange"] = "-"
                quote["ltd"] = soup.select("div.companyright span")[0].text

                quote["securityId"] = soup.select("td#tdCShortName.resultleft")[0].text
                quote["scriptCode"] = soup.select("td#tdscripcode.resultleft")[0].text
                quote["group"] = soup.select("td#tdgroup.resultleft")[0].text.split("/")[0].strip()
                quote["index"] = soup.select("td#tdgroup.resultleft")[0].text.split("/")[1].strip()
                quote["faceValue"] = soup.select("td#tdfacevalue.resultleft")[0].text
                # STOCK TRADING
                quote["previousClose"] = soup.select("td#tdpcloseopen.TTRow_right")[0].text.split(
                    "/"
                )[0]
                quote["lastOpen"] = soup.select("td#tdpcloseopen.TTRow_right")[0].text.split("/")[1]
                try:
                    quote["daysHigh"] = soup.select("td#tdDHL.TTRow_right")[0].text.split("/")[0]
                    quote["daysLow"] = soup.select("td#tdDHL.TTRow_right")[0].text.split("/")[1]
                except Exception:
                    quote["daysHigh"] = "-"
                    quote["daysLow"] = "-"
                quote["wtdAvgPrice"] = soup.select("td#tdWAp.TTRow_right")[0].text
                quote["totalTradedValue"] = {}
                quote["totalTradedValue"]["in"] = "Cr"
                quote["totalTradedValue"]["value"] = soup.select("td#tdTTV.TTRow_right")[0].text
                quote["totalTradedQty"] = {}
                quote["totalTradedQty"]["in"] = "Lac"
                quote["totalTradedQty"]["value"] = soup.select("td#tdTTQW.TTRow_right")[
                    0
                ].text.split("/")[0]
                quote["twoWeekAvgQty"] = {}
                try:
                    quote["twoWeekAvgQty"]["in"] = "Lac"
                    quote["twoWeekAvgQty"]["value"] = soup.select("td#tdTTQW.TTRow_right")[
                        0
                    ].text.split("/")[1]
                except Exception:
                    quote["twoWeekAvgQty"]["in"] = "-"
                    quote["twoWeekAvgQty"]["value"] = "-"
                quote["mktCap"] = {}
                quote["mktCap"]["in"] = "Cr"
                quote["mktCap"]["value"] = (
                    soup.select("tr#trMktCap td.TTRow_right")[0].text.split("/")[0].strip()
                )
                quote["freeFloat"] = {}
                quote["freeFloat"]["in"] = "Cr"
                quote["freeFloat"]["value"] = (
                    soup.select("tr#trMktCap td.TTRow_right")[0].text.split("/")[1].strip()
                )

                # # HIGHS AND LOWS: 1-DAY, 1-WEEK, 1-MONTH, 52-WEEK
                baseurl2 = (
                    "https://api.bseindia.com/BseIndiaAPI/api/HighLow/w?Type=EQ&flag=C&scripcode="
                )
                response2 = requests.get(baseurl2 + str(script_code), headers=bse_api_headers)
                highLow = response2.json()
                a = highLow["Fifty2WkHigh_adj"]
                b = highLow["Fifty2WkLow_adj"]
                quote["fiftytwo_WeekHigh"] = float(a)
                quote["fiftytwo_WeekLow"] = float(b)
                quote["monthHighLow"] = highLow["MonthHighLow"]
            else:
                return invalid_script_code
        else:
            return invalid_script_code
    except Exception:
        return error
    return quote


def bulk_deals(script_code: int | str) -> dict[str, Any]:
    # BULK DEALS
    try:
        # script codes are suppose to be 6 digit integers
        script_code = int(script_code)
        if len(str(script_code)) == 6:
            baseurl = (
                "https://api.bseindia.com/BseIndiaAPI/api/TabResults/w?scripcode="
                + str(script_code)
                + "&tabtype=BULK"
            )
            response = requests.get(baseurl, headers=bse_api_headers)
            bulkDeals = response.json()
            if len(bulkDeals) == 0:
                bulkDeals = error
            deals = {"bulk_deals": bulkDeals}
        else:
            return invalid_script_code
    except Exception:
        return error
    return deals


def ratios(script_code: int | str) -> dict[str, Any]:
    try:
        # script codes are suppose to be 6 digit integers
        script_code = int(script_code)
        if len(str(script_code)) == 6:
            # RATIOS: PE, EPS(TTM), CEPS, PB, ROE, FACEVALUE
            baseurl = (
                "https://api.bseindia.com/BseIndiaAPI/api/ComHeader/w?quotetype=EQ&scripcode="
                + str(script_code)
                + "&seriesid="
            )
            response = requests.get(baseurl, headers=bse_api_headers)
            ratio1 = response.json()
            if ratio1["SecurityId"] is None:
                return invalid_script_code
            # INFO(52 wk high-low with dates,Revenue,PAT,Equity) RATIOS(OPM,NPM,RONW)
            ratio3 = {}
            baseurl1 = (
                "https://api.bseindia.com/BseIndiaAPI/api/EQPeerGp/w?scripcode="
                + str(script_code)
                + "&scripcomare="
            )
            response1 = requests.get(baseurl1, headers=bse_api_headers)
            ratio2 = response1.json()
            ratio3["OPM"] = ratio2["Table"][0]["OPM"]
            ratio3["NPM"] = ratio2["Table"][0]["NPM"]
            ratio3["RONW"] = ratio2["Table"][0]["RONW"]
            ratio3["EPS"] = ratio2["Table"][0]["EPS"]
            ratio3["CEPS"] = ratio2["Table"][0]["Cash_EPS"]
            ratio3["PE"] = ratio2["Table"][0]["PE"]
            data = {"value_ratio": ratio1, "profit_ratio": ratio3}
        else:
            return invalid_script_code
    except Exception:
        return error
    return data


def peers(script_code: int | str) -> dict[str, Any]:
    try:
        # script codes are suppose to be 6 digit integers
        script_code = int(script_code)
        if len(str(script_code)) == 6:
            # PEER COMPARISON WITH INFO(52 wk high-low with dates,Revenue,PAT,Equity,Shareholdings)
            # RATIOS(OPM,NPM,RONW,EPS,CEPS,PE)
            baseurl = (
                "https://api.bseindia.com/BseIndiaAPI/api/EQPeerGp/w?scripcode="
                + str(script_code)
                + "&scripcomare="
            )
            response = requests.get(baseurl, headers=bse_api_headers)
            peer_comp = response.json()
            if peer_comp["Table"][0]["scrip_cd"] is None:
                return invalid_script_code
        else:
            return invalid_script_code
    except Exception:
        return error
    return peer_comp


def holdings(script_code: int | str) -> dict[str, Any]:
    try:
        # script codes are suppose to be 6 digit integers
        script_code = int(script_code)
        if len(str(script_code)) == 6:
            stocks_id = getScript_id(script_code, "id")
            url = (
                "https://frapi.marketsmojo.com/Stocks_Shareholding/get_results?sid="
                + str(stocks_id)
                + "&exchange=0&close_peer=undefined"
            )
            response = requests.get(url, headers=headers)
            mojo_hold = response.json()
            # CLEANING JSON
            holding_data = {}
            holding_data["holdings"] = mojo_hold["data"]["shareholding_snapshot"]
            holding_data["holding_comp"] = mojo_hold["data"]["shareholding_compare"]
            holding_data["holding_analysis"] = mojo_hold["data"]["shareholding_analysis"]
        else:
            return invalid_script_code
    except Exception:
        return error
    return holding_data


def news(script_code: int | str) -> dict[str, Any]:
    try:
        # script codes are suppose to be 6 digit integers
        script_code = int(script_code)
        if len(str(script_code)) == 6:
            stocks_id = getScript_id(script_code, "id")
            url = (
                "https://frapi.marketsmojo.com/Stocks_Priceupdates/priceupdates_info?sid="
                + str(stocks_id)
                + "&exchange=0&se=bse&cardlist=sectPrice_techScore&"
            )
            response = requests.get(url, headers=headers)
            news = response.json()
            news_data = {}
            news_data["news"] = news["data"]["NEWS"]
        else:
            return invalid_script_code
    except Exception:
        return error
    return news_data


def corporate_actions(script_code: int | str) -> dict[str, Any]:
    try:
        # script codes are suppose to be 6 digit integers
        script_code = int(script_code)
        if len(str(script_code)) == 6:
            stocks_id = getScript_id(script_code, "id")
            url = (
                "https://frapi.marketsmojo.com/Stocks_Corporateactions/Corp_action_Full_Details?sid="
                + str(stocks_id)
                + "&exchange=0&nores=null&"
            )
            response = requests.get(url, headers=headers)
            corp_act = response.json()
            # CLEANING JSON
            corp_action = {}
            corp_action["board_meetings"] = corp_act["data"][0]["data"][:3]
            corp_action["dividends"] = corp_act["data"][1]
            corp_action["splits"] = corp_act["data"][2]
            corp_action["bonus"] = corp_act["data"][3]
            corp_action["rights"] = corp_act["data"][4]
        else:
            return invalid_script_code
    except Exception:
        return error
    return corp_action


def get_profile(script_code: int | str) -> dict[str, Any]:
    # Sourced from Screener.in. (Previously scraped Yahoo Finance's /profile page,
    # which Yahoo decommissioned — it now 404s. Screener exposes the business
    # description, website and exchange links reliably; sector/industry/CEO are no
    # longer available, so those keys were dropped. See DESIGN_DECISIONS.md ADR.)
    try:
        # script codes are suppose to be 6 digit integers
        script_code = int(script_code)
        if len(str(script_code)) != 6:
            return invalid_script_code
        screener_url = getScriptUrl(script_code)
        res = requests.get("https://www.screener.in" + str(screener_url), headers=headers)
        soup = BeautifulSoup(res.text, "lxml")
        name_tag = soup.select_one("h1")
        comp_name = name_tag.get_text(strip=True) if name_tag else ""
        desc_tag = soup.select_one("div.company-profile div.about p")
        description = " ".join(desc_tag.get_text().split()) if desc_tag else ""
        # website = first external company link that isn't an exchange/screener URL
        website = ""
        for a in soup.select("div.company-links a"):
            href = str(a.get("href") or "")
            if href.startswith("http") and not any(
                d in href for d in ("bseindia", "nseindia", "screener")
            ):
                website = href
                break
        bse = soup.select_one("div.company-links a[href*='bseindia']")
        nse = soup.select_one("div.company-links a[href*='nseindia']")
        profile = {
            "script_code": script_code,
            "Name": comp_name,
            "description": description,
            "website": website,
            "bse_link": bse["href"] if bse else "",
            "nse_link": nse["href"] if nse else "",
        }
    except Exception:
        return error
    return profile
