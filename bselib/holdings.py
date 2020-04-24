import requests 
import json

def holdings(script_code):
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
            mojo_holds = requests.get('https://frapi.marketsmojo.com/Stocks_Shareholding/get_results?sid='+str(stocks_id)+'&exchange=0&close_peer=undefined')
            mojo_hold = mojo_holds.json()
            # CLEANING JSON
            mojo_holdings = mojo_hold['data']["shareholding_snapshot"]
            holding_comp = mojo_hold['data']["shareholding_compare"]
            holding_analysis = mojo_hold['data']["shareholding_analysis"]
            data = {'mojo_holdings':mojo_holdings,'holding_comp':holding_comp, 'holding_analysis':holding_analysis}
            return data
        else:
            msg = {'info':'length of script_code should be 6 digit'}
            return msg
    except:
        msg = {'info' : 'Error'}
        return msg
      