import requests
import json


# API-CALL TO GET SCRIPTCODE FOR BSE AND ID FOR STOCK ON MARKET-MOJ0
def get_script(stock): 
    try:
        mojo_url = 'https://www.marketsmojo.com/portfolio-plus/frontendsearch?SearchPhrase='
        stocks_data = requests.get(mojo_url + str(stock))
        stocks = json.loads(stocks_data.text.replace("<b>","").replace("</b>","").replace("\t","").replace("\n",""))  
        tall = len(stocks)
        if len(stocks) == 0: 
            stocks = {'info' : 'please be more specific'}
        company = []
        code = []   
        for i in range(tall):
            company.append(stocks[i]['Company'])
            code.append(stocks[i]['ScriptCode'])

        data = dict(zip(code,company))   
    except:
        msg = {'info' : 'Error'}
        return msg
    return data