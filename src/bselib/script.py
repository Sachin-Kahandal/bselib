import requests
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}

# API-CALL TO GET SCRIPTCODE FOR BSE AND ID FOR STOCK ON MARKET-MOJ0
def script(stock):
    try:
        mojo_url = 'https://www.marketsmojo.com/portfolio-plus/frontendsearch?SearchPhrase='
        response = requests.get(mojo_url + str(stock), headers=headers)
        stocks = json.loads(response.text.replace("<b>","").replace("</b>","").replace("\t","").replace("\n","")) 
        tall = len(stocks) 
        if len(stocks) == 0: 
            stocks = {'info' : 'please be more specific'}   
        company = []
        code = []   
        for i in range(tall):
            company.append(stocks[i]['Company'])
            code.append(stocks[i]['ScriptCode'])

        script_codes = dict(zip(code,company)) 
    except:
        error = {'info' : 'Error'}
        return error
    return script_codes