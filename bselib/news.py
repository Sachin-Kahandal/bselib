import requests
from bs4 import BeautifulSoup
import json


def news(script_code):
    try:
        x = int(script_code)   
        script_code = str(x)
        if len(script_code) == 6:
            mojo_url = 'https://www.marketsmojo.com/portfolio-plus/frontendsearch?SearchPhrase='
            stocks_data = requests.get(mojo_url + script_code)
            stocks = json.loads(stocks_data.text.replace("<b>", "").replace("</b>", "").replace("\t", "").replace("\n", ""))
            if len(stocks) == 0: 
                msg = {'info': 'incorrect script_code'}
            stock_id = (stocks[0]['Id'])
            stocks_id = str(stock_id)
            mojo = requests.get('https://frapi.marketsmojo.com/Stocks_Priceupdates/priceupdates_info?sid='+str(stocks_id)+'&exchange=0&se=bse&cardlist=sectPrice_techScore&')
            mojo_news = mojo.json()
            mojo_news = mojo_news['data']['NEWS']
            data = {'news':mojo_news}
            return data
        else:
            msg = {'info':'length of script_code should be 6 digit'}
            return msg
    except:
        msg = {'info' : 'Error'}
        return msg