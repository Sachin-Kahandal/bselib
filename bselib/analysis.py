import requests 
import json

def performance_analysis(script_code):
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
            mojo_url1 = 'https://frapi.marketsmojo.com/stocks_stocksid/header_info?sid='+str(stocks_id)+'&exchange=1'
            mojo_data = requests.get(mojo_url1)
            info1 = mojo_data.json()
            # CLEANING JSON
            summary = info1['data']['summary']
            data = {'analysis':summary}
            return data
        else:
            msg = {'info':'length of script_code should only be 6 digit'}
            return msg
    except:
        msg = {'info' : 'Error, please check script_code'}
        return msg