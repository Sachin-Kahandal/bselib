import requests
import json


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
invalid_script_code = {'info' : 'Not a valid script_code'}
error = {'info' : 'Error'}

def getScript_id(script_code, data):
    try:
        # script codes are suppose to be 6 digit integers
        script_code = int(script_code)   
        if len(str(script_code)) == 6:
            mojo_url = 'https://www.marketsmojo.com/portfolio-plus/frontendsearch?SearchPhrase='
            response = requests.get(mojo_url + str(script_code), headers=headers)
            stocks = json.loads(response.text.replace("<b>", "").replace("</b>", "").replace("\t", "").replace("\n", ""))
            if len(stocks) == 0:
                return invalid_script_code
            if data == "id":
                stock_id = (stocks[0]['Id'])
                data = str(stock_id)
            else:
                stock_id = (stocks[0]['Company'])
                data = str(stock_id).split("-")[0].strip()
            return data
        else:
            return invalid_script_code
    except:
        return error


def getScriptUrl(script_code):
    try:
        script_code = int(script_code)
        if len(str(script_code)) == 6:
            baseurl = 'https://www.screener.in/api/company/search/?q='
            url = (baseurl + str(script_code))
            response = requests.get(url, headers=headers)
            stocks = response.json()
            screener_url = stocks[0]['url'].strip()
            if len(screener_url) == 0: 
                return invalid_script_code
        else:
            return invalid_script_code
    except:
        return error
    return screener_url