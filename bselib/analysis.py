import requests 
from bs4 import BeautifulSoup
import json
from bselib.getId import getScript_id, getScriptUrl


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
invalid_script_code = {'info' : 'Not a valid script_code'}
error = {'info' : 'Error'}

def analysis(script_code):
    try:
        # marketmojo uses its own ids for stocks
        stocks_id = getScript_id(script_code,"id")
        # stock's summary analysis 
        mojo_url1 = 'https://frapi.marketsmojo.com/stocks_stocksid/header_info?sid='+str(stocks_id)+'&exchange=1'
        mojo_response1 = requests.get(mojo_url1,headers=headers)
        info1 = mojo_response1.json()
        # cleaning json
        summary = info1['data']['summary']
        # stock's value analysis
        mojo_url2 = 'https://frapi.marketsmojo.com/stocks_dashboard/stockinfo?sid='+str(stocks_id)+'&callback=?'
        mojo_response2 = requests.get(mojo_url2,headers=headers)
        info2 = mojo_response2.json()
        # cleaning json
        value_analysis = dict()
        value_analysis['quality'] = info2['data']['quality']
        value_analysis['valuation'] = info2['data']['valuation']
        value_analysis['technicals'] = info2['data']['technicals']
        value_analysis['technicaltext'] = info2['data']['technicaltext']
        value_analysis['fintrend'] = info2['data']['fintrend']
        value_analysis['overview'] = info2['data']['maintext']
        # stock's pros and cons from screener.in 
        screener_url = getScriptUrl(script_code)
        screener_url = 'https://www.screener.in'+str(screener_url)
        res = requests.get(screener_url, headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')

        pros, cons = list(), list()
        con = soup.select("div.warning")
        pro = soup.select("div.success")
        for tag in con:
            cons = tag.text.strip().replace('Cons:','').replace('\n',' ')
        for tag in pro:
            pros = tag.text.strip().replace('\n',' ').replace('Pros:','')
        # getting all data in a dictionary
        data = {'value_analysis':value_analysis, 'price_analysis':summary, 'pros' : pros, 'cons' : cons }
    except:
        return error
    return data


def stmt_analysis(script_code, stats):
    try:
        stocks_id = getScript_id(script_code,"id")
        if stats == 'quarter_results':
            mojo_url1 = 'https://frapi.marketsmojo.com/Stocks_Periodicresults/get_results?sid='+str(stocks_id)+'&exchange=0&period=q&page=1&cards=11'
            mojo_response1 = requests.get(mojo_url1, headers=headers)
            info1 = mojo_response1.json()
            # cleaning json
            qoq = info1['data'][1]
            yoy = info1['data'][5]
            return qoq, yoy

        elif stats == 'yoy_results':
            mojo_url2 = 'https://frapi.marketsmojo.com/Stocks_Periodicresults/get_results?sid='+str(stocks_id)+'&exchange=0&period=y&page=1&cards=11'
            mojo_response2 = requests.get(mojo_url2, headers=headers)
            info2 = mojo_response2.json()
            # cleaning json
            yoy_results = info2['data'][1]
            return yoy_results

        elif stats == 'balancesheet':
            mojo_url3 = 'https://frapi.marketsmojo.com/Stocks_Balancesheet/get_results?sid='+str(stocks_id)+'&exchange=0&period=y&page=1&cards=11'
            mojo_data3 = requests.get(mojo_url3, headers=headers)
            info3 = mojo_data3.json()
            # cleaning json
            bal_sheet_analysis = info3['data'][1]
            yoy_bal_sheet = {'bal_analysis':bal_sheet_analysis}
            return yoy_bal_sheet
        
        elif stats == 'profitloss':
            mojo_url4 = 'https://frapi.marketsmojo.com/Stocks_Profitloss/get_results?sid='+str(stocks_id)+'&exchange=0&period=y&page=1&cards=11'
            mojo_response4 = requests.get(mojo_url4, headers=headers)
            info4 = mojo_response4.json()
            # cleaning json
            yoy_pl = info4['data'][1]
            return yoy_pl

        elif stats == 'cashflow':
            mojo_url5 = 'https://frapi.marketsmojo.com/Stocks_Profitloss/get_results?sid='+str(stocks_id)+'&exchange=0&period=y&page=1&cards=11'
            mojo_response5 = requests.get(mojo_url5, headers=headers)
            info5 = mojo_response5.json()
            # CLEANING JSON
            cf_analysis = info5['data'][1]
            cf_yoy = {'cf_analysis':cf_analysis}
            return cf_yoy
        else:
            return {"error" : "select either of these statements: cashflow, yoy_results, profitloss, quarter_results, balancesheet"}
    except:
        return error