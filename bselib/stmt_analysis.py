from bs4 import BeautifulSoup
import requests
import json


def stmt_analysis(script_code):
    try:
        x = int(script_code)   
        script_code = str(x)
        if len(script_code) == 6:
            mojo_url = 'https://www.marketsmojo.com/portfolio-plus/frontendsearch?SearchPhrase='
            stocks_url = requests.get(mojo_url + script_code)
            stocks = json.loads(stocks_url.text.replace("<b>", "").replace("</b>", "").replace("\t", "").replace("\n", ""))
            if len(stocks) == 0: 
                msg = {'info': 'incorrect script_code'}
            stock_id = (stocks[0]['Id'])
            stocks_id = str(stock_id)
            mojo_url1 = 'https://frapi.marketsmojo.com/Stocks_Periodicresults/get_results?sid='+str(stocks_id)+'&exchange=0&period=q&page=1&cards=11'
            mojo_data1 = requests.get(mojo_url1)
            info1 = mojo_data1.json()
            # CLEANING JSON
            qoq = info1['data'][1]
            yoy = info1['data'][5]
            mojo_data2 = requests.get('https://frapi.marketsmojo.com/Stocks_Periodicresults/get_results?sid='+str(stocks_id)+'&exchange=0&period=y&page=1&cards=11')
            info2 = mojo_data2.json()
            # CLEANING JSON
            yoy1 = info2['data'][1]
            mojo_data3 = requests.get('https://frapi.marketsmojo.com/Stocks_Balancesheet/get_results?sid='+(stocks_id)+'&exchange=0&period=y&page=1&cards=11')
            info3 = mojo_data3.json()
            # CLEANING JSON
            bal_sheet_analysis = info3['data'][1]
            mojo_data4 = requests.get('https://frapi.marketsmojo.com/Stocks_Profitloss/get_results?sid='+(stocks_id)+'&exchange=0&period=y&page=1&cards=11')
            info4 = mojo_data4.json()
            # CLEANING JSON
            pl_analysis = info4['data'][1]
            mojo_data5 = requests.get('https://frapi.marketsmojo.com/Stocks_Cashflow/get_results?sid='+(stocks_id)+'&exchange=0&period=y&page=1&cards=11')
            info5 = mojo_data5.json()
            # CLEANING JSON
            cf_analysis = info5['data'][1]
            data = {'qrt_qoq_analysis':qoq, 'qrt_yoy_analysis':yoy, 'yr_analysis':yoy1, 'bal_analysis':bal_sheet_analysis,
            'pl_analysis':pl_analysis,'cf_analysis':cf_analysis}
            return data
        else:
            msg = {'info':'length of script_code should only be 6 digit'}
            return msg
    except:
        msg = {'info' : 'Error'}
        return msg