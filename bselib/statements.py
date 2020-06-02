from bs4 import BeautifulSoup
import requests
from pandas import read_html
from bselib.getId import getScriptUrl


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
baseurl = 'https://www.screener.in'
invalid_script_code = {'info':'Not a valid script_code'}
error = {'info':'Error'}


def historical_stats(script_code, stats):
    screener_url = getScriptUrl(script_code)
    try: 
        df = read_html(baseurl + str(screener_url), index_col=None)
        # QUARTERLY RESULTS
        if stats == 'quarter_results':
            quarter_res = df[0].to_dict()
            return quarter_res
        # PROFIT-LOSS STATEMENTS
        elif stats == 'yoy_results':
            yoy_res = df[1].to_dict()
            return yoy_res
        # BALANCESHEETS
        elif stats == 'balancesheet':
            bal_sheets = df[6].to_dict()
            return bal_sheets
        # CASHFLOW
        elif stats == 'cashflow':
            cash_flow = df[7].to_dict()
            return cash_flow
        else:
            return {"error" : "select either of these statements: cashflow, yoy_results, quarter_results, balancesheet" }
    except:
        return error    
    

def statement(script_code, stats):
    screener_url = getScriptUrl(script_code)
    try:
        res = requests.get(baseurl + str(screener_url), headers=headers)
        soup = BeautifulSoup(res.text, 'lxml')
        head = ['sales','expenses','operating_profit','opm','other_income','interest','depreciation',
            'profit_before_tax','tax_percentage','net_profit','eps']
        item = list()
        #  quarter results
        if stats == 'quarter_results':
            latest_qrt = soup.select('section#quarters td:nth-of-type(8)')
            for i in range(0,len(head)):
                item.append(latest_qrt[i].text)

            qrt_res = dict(zip(head,item))
            return qrt_res

        #  ttm results 
        elif stats == 'ttm_results':
            ttm_pl = soup.select('section#profit-loss td:nth-of-type(12)')
            for i in range(0,len(head)):
                item.append(ttm_pl[i].text)

            pl_ttm = dict(zip(head,item))
            return pl_ttm

        # yoy results
        elif stats == 'yoy_results':
            yoy_pl = soup.select('section#profit-loss td:nth-of-type(11)')
            for i in range(0,len(head)):
                item.append(yoy_pl[i].text)

            pl_yoy = dict(zip(head,item))
            return pl_yoy

        # balancesheet statement
        elif stats == 'balancesheet':
            yoy_bal = soup.select('section#balance-sheet td:nth-of-type(12)')
            head = ['share_capital','reserves','borrowings','other_liabilities','total_liabilities','fixed_assets','CWIP','investments','other_assets','total_assets']
            for i in range(0,len(head)):
                item.append(yoy_bal[i].text)

            yoy_bal_sheet = dict(zip(head,item))
            return yoy_bal_sheet

        # cashflow statement
        elif stats == 'cashflow':
            yoy_cf = soup.select('section#cash-flow td:nth-of-type(11)')
            head = ['Cash from operating activity','Cash from investing activity','Cash from finance activity']
            for i in range(0,len(head)):
                item.append(yoy_cf[i].text)

            cf_yoy = dict(zip(head,item))
            return cf_yoy
        else:
            return {"info" : "select either of these statements: cashflow, yoy_results, quarter_results, balancesheet" }
    except:
        return error

def annual_reports(script_code):
    try:
        screener_url = getScriptUrl(script_code)
        res = requests.get(baseurl + str(screener_url), headers=headers)
        soup = BeautifulSoup(res.content, 'lxml') 
        # ANNUAL REPORT LINKS
        link_text, links, data, data_text = list(), list(), list(), list()
        for j in range(1,6):
            for link in soup.select("div.three:nth-of-type(2) li:nth-of-type("+str(j)+") a"):
                data = (link['href'])
                links.append(data)
                data_text = link.text.strip().replace("\n","")
                link_text.append(data_text)
        annual_reports =  dict(zip(link_text, links))
    except:
        return error
    return annual_reports


def credit_reports(script_code):
    try:
        screener_url = getScriptUrl(script_code)
        res = requests.get(baseurl + str(screener_url), headers=headers)
        soup = BeautifulSoup(res.content, 'lxml') 
        # CREDIT-RATINGS REPORT LINKS
        link_text, links, data, data_text, count = list(), list(), list(), list(), int()
        count = len(soup.select("div.three:nth-of-type(3) a"))
        for j in range(1,count+1):
            for link in soup.select("div.three:nth-of-type(3) li:nth-of-type("+str(j)+") a"):
                data = (link['href'])
                links.append(data)
                data_text = link.text.strip().replace("\n","")
                link_text.append(data_text)
        credit_ratings = dict(zip(link_text, links))
    except:
        return error
    return credit_ratings