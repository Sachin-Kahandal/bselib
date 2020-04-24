import requests 
import json

def comp_details(script_code):
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
            mojo = requests.get('https://frapi.marketsmojo.com/Stocks_Companycv/get_company_cv_data?sid='+str(stocks_id)+'&exchange=0&')
            mojo_kyc = mojo.json()
            mojo_kyc = mojo_kyc['data']['KNOW_YOUR_COMPANY']
            data = {'info':mojo_kyc}
            return data
        else:
            msg = {'info':'length of script_code should be 6 digit'}
            return msg
    except:
        msg = {'info' : 'Error'}
        return msg